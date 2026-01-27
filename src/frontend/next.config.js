/** @type {import('next').NextConfig} */
const nextConfig = {
  // 本番デプロイ用のスタンドアロン出力
  output: 'standalone',

  // 実験的機能
  experimental: {
    // Server Actionsを有効化
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },

  // 環境変数
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },

  // 画像最適化設定
  images: {
    remotePatterns: [],
  },

  // リダイレクト設定
  async redirects() {
    return [];
  },

  // リライト設定（APIプロキシ用）
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
