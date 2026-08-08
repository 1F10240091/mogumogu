"""アプリケーション設定。

環境変数 / backend/.env から読み込む。本番環境（APP_ENV=production）では
安全でないデフォルト値が使われないように起動時に検証する。
"""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent

# ローカル開発用のシードシークレット（本番では必ず .env で上書きする）
_DEV_JWT_SECRET = "dev-only-change-me-0123456789abcdef0123456789abcdef"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(BACKEND_DIR / ".env"), env_file_encoding="utf-8")

    app_name: str = "MoguMogu API"
    version: str = "0.1.0"
    app_env: str = "development"  # development | production

    database_url: str = f"sqlite:///{BACKEND_DIR / 'hoiku_recipe.db'}"
    jwt_secret_key: str = _DEV_JWT_SECRET
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    # カンマ区切りで複数指定可: http://localhost:3000,https://example.com
    cors_origins_raw: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_origins_raw.split(",") if o.strip()]

    # レート制限（ログイン・登録へのブルートフォース対策）
    rate_limit_enabled: bool = True
    rate_limit_max_requests: int = 5
    rate_limit_window_seconds: int = 60

    # AI 献立生成 / 画像 OCR（Gemini などの OpenAI 互換 API）
    ai_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    ai_model: str = "gemini-2.5-flash"
    ai_api_key: str = ""
    ai_timeout_seconds: int = 120

    def validate_for_production(self) -> None:
        """本番（APP_ENV=production）で危険な設定が残っていないか検査する。"""
        if self.app_env != "production":
            return
        if not self.jwt_secret_key or self.jwt_secret_key == _DEV_JWT_SECRET:
            raise ValueError(
                "本番環境では JWT_SECRET_KEY を .env に必ず設定してください（デフォルト値は禁止）。"
            )
        if len(self.jwt_secret_key) < 32:
            raise ValueError("JWT_SECRET_KEY は 32 文字以上にしてください。")
        if {"http://localhost:3000", "http://localhost:8000"} & set(self.cors_origins):
            raise ValueError(
                "本番環境では CORS_ORIGINS に localhost を指定しないでください。"
            )
        if "sqlite" in self.database_url:
            raise ValueError(
                "本番環境では SQLite を使用できません（DATABASE_URL に PostgreSQL 等を設定してください）。"
            )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_for_production()
    return settings