"""
共通ユーティリティ関数
アプリケーション全体で使用する汎用的な関数を提供
"""

from datetime import datetime, timedelta
from typing import Optional

from config import settings


def is_within_edit_period(created_at: datetime) -> bool:
    """
    作成日時が編集可能期間内かチェック

    Args:
        created_at: 作成日時

    Returns:
        編集可能な場合True、期限切れの場合False
    """
    now = datetime.utcnow()
    days_passed = (now - created_at).days
    return days_passed <= settings.report_edit_days_limit


def get_edit_deadline(created_at: datetime) -> datetime:
    """
    編集期限の日時を取得

    Args:
        created_at: 作成日時

    Returns:
        編集期限の日時
    """
    return created_at + timedelta(days=settings.report_edit_days_limit)


def normalize_email(email: str) -> str:
    """
    メールアドレスを正規化（小文字化）

    Args:
        email: メールアドレス

    Returns:
        正規化されたメールアドレス
    """
    return email.lower().strip()


def format_phone_number(phone: Optional[str]) -> Optional[str]:
    """
    電話番号のフォーマット（ハイフン除去）

    Args:
        phone: 電話番号

    Returns:
        フォーマット済み電話番号
    """
    if not phone:
        return None
    return phone.replace("-", "").replace(" ", "").strip()
