"""pytest フィクスチャ。

テスト用に一時 SQLite DB を使用し、テストごとにデータを分離する。
"""

import os
import sys
import uuid
from pathlib import Path

import pytest

# テスト用 DB パスを最優先で設定（リポジトリ直下の一時領域に置く）
TEST_DB = Path(__file__).resolve().parent.parent / ".test_hoiku_recipe.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB}"
os.environ["AI_API_KEY"] = ""  # テストではルールベースを使用
os.environ["RATE_LIMIT_ENABLED"] = "false"  # テストではレート制限を無効化（専用テストで検証）

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.services.seed import seed_recipes  # noqa: E402


@pytest.fixture(scope="session")
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_recipes(db)
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_client(client):
    """一意メールで登録済みユーザーのトークンを付与したクライアントを返す。

    セッション共有の client はヘッダを汚染しないよう、専用の TestClient を作る。
    """
    email = f"user-{uuid.uuid4().hex[:12]}@example.com"
    res = TestClient(app)
    r = res.post("/api/v1/auth/register", json={"email": email, "password": "password123"})
    assert r.status_code == 201, r.text
    token = r.json()["access_token"]
    res.headers.update({"Authorization": f"Bearer {token}"})
    return res
