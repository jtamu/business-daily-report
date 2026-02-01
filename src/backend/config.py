"""
アプリケーション設定管理モジュール
環境変数から設定を読み込み、型安全な設定クラスを提供
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """アプリケーション設定"""

    # アプリケーション基本設定
    app_name: str = "営業日報システム API"
    app_version: str = "1.0.0"
    debug: bool = False

    # サーバー設定
    host: str = "0.0.0.0"
    port: int = 8000

    # データベース設定
    database_url: str = "postgresql://user:password@localhost:5432/business_report"
    database_echo: bool = False  # SQLAlchemyのSQL出力を有効化（開発時のみ推奨）

    # JWT認証設定
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60  # 1時間

    # CORS設定
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    # ログ設定
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # ページネーション設定
    default_page_size: int = 20
    max_page_size: int = 100

    # ビジネスルール設定
    report_edit_days_limit: int = 7  # 日報の編集可能期間（日）

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# シングルトンインスタンス
settings = Settings()
