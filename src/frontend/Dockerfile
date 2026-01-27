# ============================================
# 営業日報システム - フロントエンド Dockerfile
# Node.js 20.x + Next.js (App Router)
# ============================================

# ============================================
# Base Stage: 共通の設定
# ============================================
FROM node:20-alpine as base

# 環境変数の設定
ENV NODE_ENV=development

WORKDIR /app

# パッケージマネージャーの設定
RUN corepack enable && corepack prepare pnpm@latest --activate

# ============================================
# Dependencies Stage: 依存関係のインストール
# ============================================
FROM base as deps

# package.jsonとロックファイルをコピー
COPY package.json pnpm-lock.yaml* package-lock.json* yarn.lock* ./

# 依存関係のインストール
RUN \
    if [ -f pnpm-lock.yaml ]; then pnpm install --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    elif [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
    else npm install; \
    fi

# ============================================
# Development Stage: 開発環境
# ============================================
FROM base as development

WORKDIR /app

# 依存関係をコピー
COPY --from=deps /app/node_modules ./node_modules
COPY package.json ./

# ソースコードはボリュームマウントで参照するため、ここではコピーしない
# ホットリロード対応

EXPOSE 3000

# 開発サーバー起動
CMD ["npm", "run", "dev"]

# ============================================
# Builder Stage: 本番用ビルド
# ============================================
FROM base as builder

WORKDIR /app

# 依存関係をコピー
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# 本番用環境変数
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# ビルド実行
RUN npm run build

# ============================================
# Production Stage: 本番環境
# ============================================
FROM node:20-alpine as production

WORKDIR /app

# 非rootユーザーの作成
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# 本番用環境変数
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# ビルド成果物をコピー（standaloneモードを使用）
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# 非rootユーザーに切り替え
USER nextjs

EXPOSE 3000

# 本番サーバー起動
CMD ["node", "server.js"]
