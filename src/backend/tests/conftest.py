"""
pytestの共通設定とフィクスチャ
テスト全体で使用する共通の設定や前処理を定義
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import settings
from db.database import Base, get_db
from main import app

# テスト用データベースURL（SQLiteを使用）
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# テスト用エンジンとセッションの作成
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite用の設定
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    テスト用データベースセッション
    各テスト関数ごとに新しいセッションを作成し、テスト後にロールバック
    """
    # テスト用のテーブルを作成
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        # テスト後にテーブルを削除
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session):
    """
    テスト用FastAPIクライアント
    データベースセッションを注入したクライアントを返す
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user_data():
    """テスト用ユーザーデータ"""
    return {
        "name": "テストユーザー",
        "email": "test@example.com",
        "password": "Test1234!",
        "role": "staff",
    }


@pytest.fixture(scope="function")
def test_manager_data():
    """テスト用上長データ"""
    return {
        "name": "テスト上長",
        "email": "manager@example.com",
        "password": "Test1234!",
        "role": "manager",
    }


@pytest.fixture(scope="function")
def test_customer_data():
    """テスト用顧客データ"""
    return {
        "company_name": "株式会社テスト",
        "contact_person": "テスト太郎",
        "phone": "03-1234-5678",
        "email": "test@test.co.jp",
        "address": "東京都千代田区1-2-3",
    }


@pytest.fixture(scope="session")
def app_settings():
    """アプリケーション設定"""
    return settings
