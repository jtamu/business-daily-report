"""
営業日報システム - バックエンドAPIエントリーポイント
FastAPI アプリケーション
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from logger import app_logger
from middleware.errors import (
    BusinessException,
    business_exception_handler,
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    アプリケーションのライフサイクル管理
    起動時と終了時の処理を定義
    """
    # 起動時の処理
    app_logger.info("=" * 50)
    app_logger.info(f"{settings.app_name} を起動しています...")
    app_logger.info(f"バージョン: {settings.app_version}")
    app_logger.info(f"環境: {'開発' if settings.debug else '本番'}")
    app_logger.info(f"ログレベル: {settings.log_level}")
    app_logger.info("=" * 50)

    yield

    # 終了時の処理
    app_logger.info("=" * 50)
    app_logger.info(f"{settings.app_name} を停止しています...")
    app_logger.info("=" * 50)


# FastAPIアプリケーションのインスタンス化
app = FastAPI(
    title=settings.app_name,
    description="営業担当者が日々の顧客訪問活動を記録し、上長がフィードバックを提供するシステムのAPI",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    debug=settings.debug,
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# エラーハンドラーの登録
app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# ========== ルートエンドポイント ==========


@app.get("/", tags=["General"])
async def root():
    """
    ルートエンドポイント
    APIの基本情報を返す
    """
    return {
        "message": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["General"])
async def health_check():
    """
    ヘルスチェックエンドポイント
    サーバーの稼働状態を確認する
    """
    return {
        "status": "healthy",
        "version": settings.app_version,
    }


# ========== APIルーターの登録 ==========
# 注: 各APIエンドポイントは別途実装してインクルードする
# 例: app.include_router(auth_router, prefix="/auth", tags=["認証"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
