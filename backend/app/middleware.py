"""レート制限ミドルウェア。

ログイン試行などの認証関連エンドポイントを IP ごとに制限する。
プロセス内のインメモリ実装のため、複数プロセス構成では不正確になるが、
学内・学祭向けアプリとしては十分な抑止力となる。
"""

import time
from collections import defaultdict, deque
from typing import Callable

from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import Request, Response
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Starlette, max_requests: int = 5, window_seconds: int = 60) -> None:
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, deque] = defaultdict(deque)

    def _client_key(self, request: Request) -> str:
        # uvicorn を直接公開する設定（--proxy-headers なし）では
        # x-forwarded-for をクライアントが偽装できるため、優先せず接続元IPを使う。
        # リバースプロキシ（nginx 等）を使用し、--proxy-headers を有効化している場合は
        # uvicorn 側で信頼したヘッダに置換されるため request.client.host が正しい IP になる。
        if request.client is not None and request.client.host:
            return request.client.host
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return "unknown"

    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        path = request.url.path
        # レート制限を適用するエンドポイント
        limited_paths = {"/api/v1/auth/login", "/api/v1/auth/register"}
        if path not in limited_paths:
            return await call_next(request)

        key = f"{self._client_key(request)}:{path}"
        now = time.monotonic()
        hits = self._hits[key]

        # ウィンドウ外の古い記録を除去
        while hits and now - hits[0] > self.window_seconds:
            hits.popleft()

        if len(hits) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "試行回数が多すぎます。しばらく待ってから再度お試しください。"},
            )

        hits.append(now)
        return await call_next(request)
