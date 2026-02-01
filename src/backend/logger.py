"""
ロギング設定モジュール
アプリケーション全体で使用するロガーの設定
"""

import logging
import sys
from typing import Optional

from config import settings


def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    ロガーをセットアップして返す

    Args:
        name: ロガー名（省略時はルートロガー）

    Returns:
        設定済みのロガーインスタンス
    """
    logger = logging.getLogger(name)

    # 既にハンドラが設定されている場合は再設定しない
    if logger.handlers:
        return logger

    # ログレベルを設定
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # コンソールハンドラを作成
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # フォーマッタを作成
    formatter = logging.Formatter(
        settings.log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # ハンドラをロガーに追加
    logger.addHandler(console_handler)

    # 親ロガーへの伝播を無効化（重複ログ防止）
    logger.propagate = False

    return logger


# アプリケーション全体で使用するデフォルトロガー
app_logger = setup_logger("business_report")
