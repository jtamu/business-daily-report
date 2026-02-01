"""
データベース接続とセッション管理
SQLAlchemyの設定と依存性注入用の関数を提供
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from config import settings
from logger import app_logger

# データベースエンジンを作成
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,  # SQL出力の有効化/無効化
    pool_pre_ping=True,  # 接続プールの健全性チェック
    pool_size=5,  # 接続プールのサイズ
    max_overflow=10,  # 接続プールの最大オーバーフロー
)

# セッションファクトリを作成
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ベースクラスを作成（全てのモデルがこれを継承）
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    データベースセッションの依存性注入用関数
    FastAPIのDependsで使用する

    Yields:
        データベースセッション

    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        app_logger.error(f"データベースセッションエラー: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    データベースの初期化
    全てのテーブルを作成する（開発環境のみ推奨）
    本番環境ではAlembicマイグレーションを使用すること
    """
    app_logger.info("データベーステーブルを作成します...")
    Base.metadata.create_all(bind=engine)
    app_logger.info("データベーステーブルの作成が完了しました")


def drop_db() -> None:
    """
    全てのテーブルを削除（テスト環境のみ使用）
    注意: 本番環境では絶対に使用しないこと
    """
    app_logger.warning("データベーステーブルを削除します...")
    Base.metadata.drop_all(bind=engine)
    app_logger.warning("データベーステーブルの削除が完了しました")
