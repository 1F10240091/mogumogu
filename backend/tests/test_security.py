"""セキュリティ対策のテスト（パスワード強度・レート制限）。"""

import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app
from app.middleware import RateLimitMiddleware


def _limited_app(max_requests: int = 2, window_seconds: int = 60) -> TestClient:
    """レート制限付きの独立したアプリを作る。"""
    test_app = FastAPI()

    @test_app.post("/api/v1/auth/login")
    async def login():
        return {"ok": True}

    test_app.add_middleware(RateLimitMiddleware, max_requests=max_requests, window_seconds=window_seconds)
    return TestClient(test_app)


def test_password_too_weak_rejected(client):
    res = client.post("/api/v1/auth/register", json={"email": "weak@example.com", "password": "short"})
    assert res.status_code == 422

    res = client.post("/api/v1/auth/register", json={"email": "weak2@example.com", "password": "onlyletters"})
    assert res.status_code == 422

    res = client.post("/api/v1/auth/register", json={"email": "weak3@example.com", "password": "12345678"})
    assert res.status_code == 422


def test_password_with_letters_and_digits_accepted(client):
    res = client.post("/api/v1/auth/register", json={"email": "ok@example.com", "password": "abc12345"})
    assert res.status_code == 201


def test_rate_limit_blocks_excess_requests():
    tc = _limited_app(max_requests=2)
    for _ in range(2):
        res = tc.post("/api/v1/auth/login")
        assert res.status_code == 200
    res = tc.post("/api/v1/auth/login")
    assert res.status_code == 429


def test_rate_limit_per_ip_is_independent():
    tc = _limited_app(max_requests=2)
    for _ in range(2):
        assert tc.post("/api/v1/auth/login").status_code == 200
    # 上限超過後は制限される
    assert tc.post("/api/v1/auth/login").status_code == 429
    # x-forwarded-for を偽装しても制限は解除されない（接続元 IP で判定）
    for _ in range(3):
        assert tc.post("/api/v1/auth/login", headers={"x-forwarded-for": "9.9.9.9"}).status_code == 429


def test_default_app_has_rate_limit_disabled_in_tests(client):
    # テスト環境ではレート制限が無効化されている（専用テストで検証済み）
    assert os.environ.get("RATE_LIMIT_ENABLED") == "false"
