"""
メインアプリケーションのテスト
基本的なエンドポイントの動作確認
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_read_root(client: TestClient):
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert data["docs"] == "/docs"


@pytest.mark.unit
def test_health_check(client: TestClient):
    """ヘルスチェックエンドポイントのテスト"""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.unit
def test_openapi_schema(client: TestClient):
    """OpenAPIスキーマが取得できることを確認"""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data
