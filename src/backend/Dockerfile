# ============================================
# 営業日報システム - バックエンド Dockerfile
# Python 3.11 + FastAPI + Uvicorn
# ============================================

# ============================================
# Base Stage: 共通の設定
# ============================================
FROM python:3.11-slim as base

# 環境変数の設定
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# システム依存パッケージのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# Development Stage: 開発環境
# ============================================
FROM base as development

# 開発用の依存パッケージをインストール
COPY requirements.txt requirements-dev.txt* ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi

# ソースコードはボリュームマウントで参照するため、ここではコピーしない
# ホットリロード用にuvicornを--reloadオプションで起動

EXPOSE 8000

# 開発サーバー起動（ホットリロード有効）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================
# Builder Stage: 本番用ビルド
# ============================================
FROM base as builder

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# ============================================
# Production Stage: 本番環境
# ============================================
FROM python:3.11-slim as production

# 環境変数の設定
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# 最小限のシステム依存パッケージのみインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash appuser

# ビルド済みのwheelからパッケージをインストール
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

# アプリケーションコードをコピー
COPY --chown=appuser:appuser . .

# 非rootユーザーに切り替え
USER appuser

EXPOSE 8000

# 本番サーバー起動（プロキシ対応）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
