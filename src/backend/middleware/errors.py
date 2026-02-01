"""
エラーハンドリングミドルウェア
カスタム例外とエラーレスポンスの統一化
"""

from typing import Any, Dict, List, Optional

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """エラー詳細"""

    field: Optional[str] = None
    message: str


class ErrorResponse(BaseModel):
    """エラーレスポンス"""

    code: str
    message: str
    details: Optional[List[ErrorDetail]] = None


# ========== カスタム例外 ==========


class BusinessException(Exception):
    """ビジネスロジック例外の基底クラス"""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[List[ErrorDetail]] = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []
        super().__init__(message)


class ValidationException(BusinessException):
    """バリデーションエラー"""

    def __init__(self, message: str, details: Optional[List[ErrorDetail]] = None):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details,
        )


class UnauthorizedException(BusinessException):
    """認証エラー"""

    def __init__(self, message: str = "認証に失敗しました"):
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class ForbiddenException(BusinessException):
    """権限エラー"""

    def __init__(self, message: str = "この操作を実行する権限がありません"):
        super().__init__(
            code="FORBIDDEN",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class NotFoundException(BusinessException):
    """リソースが見つからない"""

    def __init__(self, message: str = "指定されたリソースが見つかりません"):
        super().__init__(
            code="NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


class DuplicateException(BusinessException):
    """重複エラー"""

    def __init__(self, message: str):
        super().__init__(
            code="DUPLICATE_ERROR",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class EditPeriodExpiredException(BusinessException):
    """編集期限切れエラー"""

    def __init__(self, message: str = "編集期限が過ぎています"):
        super().__init__(
            code="EDIT_PERIOD_EXPIRED",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


# ========== エラーハンドラー ==========


async def business_exception_handler(
    request: Request, exc: BusinessException
) -> JSONResponse:
    """ビジネス例外ハンドラー"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": [detail.model_dump() for detail in exc.details]
                if exc.details
                else None,
            }
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """FastAPIのバリデーションエラーハンドラー"""
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"][1:])  # bodyやpathを除外
        details.append(
            ErrorDetail(
                field=field if field else None,
                message=error["msg"],
            )
        )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "入力値が不正です",
                "details": [detail.model_dump() for detail in details],
            }
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTPException ハンドラー"""
    # エラーコードのマッピング
    code_mapping = {
        status.HTTP_400_BAD_REQUEST: "BAD_REQUEST",
        status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
        status.HTTP_403_FORBIDDEN: "FORBIDDEN",
        status.HTTP_404_NOT_FOUND: "NOT_FOUND",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "INTERNAL_ERROR",
    }

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code_mapping.get(exc.status_code, "UNKNOWN_ERROR"),
                "message": exc.detail,
            }
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """一般的な例外ハンドラー（予期しないエラー）"""
    # 本番環境では詳細なエラーメッセージを隠す
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "サーバー内部エラーが発生しました",
            }
        },
    )
