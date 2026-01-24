# 営業日報システム - プロジェクト概要

このドキュメントは、営業日報システムのプロジェクト全体を説明するマスタードキュメントです。
AI開発アシスタント（Claude Code）がプロジェクトを理解するために、すべての設計ドキュメントを参照しています。

## プロジェクト概要

営業担当者が日々の顧客訪問活動を記録し、課題や計画を報告するシステムです。
上長はこれらの報告を確認し、フィードバックをコメントとして提供できます。

### 主要機能
- 日報の作成・編集・閲覧（Problem/Plan記載、複数の顧客訪問記録を追加可能）
- 上長によるコメント機能
- 顧客マスタ管理
- 営業マスタ管理（上長のみ）
- 役割ベースのアクセス制御（一般営業/上長）

---

## ドキュメント構成

このプロジェクトの設計ドキュメントは以下の4つで構成されています。

### 1. 要件定義書
@docs/requirements.md

システムの機能要件とデータ要件を定義しています。
- システム概要
- 機能要件（日報作成、訪問記録、コメント機能）
- データベース設計（5つのテーブル定義）
- ER図（mermaid形式）
- リレーションシップ詳細
- 補足事項（権限管理、データ整合性、将来的な拡張性）

### 2. 画面定義書
@docs/screen-design.md

全10画面の詳細な仕様を定義しています。
- 画面一覧（SC-01〜SC-10）
- 各画面の項目定義、バリデーション、操作フロー
- 画面遷移図（mermaid形式）
- 共通仕様（ヘッダー、メッセージ表示、ページング）
- 非機能要件（パフォーマンス、セキュリティ、ブラウザ対応）

### 3. API仕様書
@docs/api-specification.yaml

OpenAPI 3.0形式のRESTful API仕様です。
- 認証API（JWT Bearer認証）
- 日報管理API
- 訪問記録API
- コメントAPI
- 顧客マスタAPI
- 営業マスタAPI
- スキーマ定義、エラーレスポンス

### 4. API使用ガイド
@docs/api-guide.md

API仕様書の補足ガイドです。
- エンドポイント一覧表
- 認証フロー（JWTトークンの取得と使用方法）
- 実際の使用例（curlコマンド）
- ページネーション仕様
- エラーハンドリング
- 権限制御マトリックス
- ビジネスルール

### 5. テスト仕様書
@docs/test-specification.md

包括的なテスト計画とテストケースを定義しています。
- テスト計画（範囲、環境、テストデータ）
- 機能テスト（90以上のテストケース）
- APIテスト
- バリデーションテスト
- 権限テスト
- 非機能テスト（パフォーマンス、セキュリティ、ブラウザ互換性）
- データ整合性テスト
- テスト完了基準

---

## プロジェクト構造

```
business-daily-report/
├── docs/                          # 設計ドキュメント
│   ├── requirements.md            # 要件定義書
│   ├── screen-design.md           # 画面定義書
│   ├── api-specification.yaml     # API仕様書（OpenAPI形式）
│   ├── api-guide.md               # API使用ガイド
│   └── test-specification.md      # テスト仕様書
├── src/                           # ソースコード（未実装）
│   ├── backend/                   # バックエンド
│   │   ├── api/                   # APIエンドポイント
│   │   ├── models/                # データモデル
│   │   ├── services/              # ビジネスロジック
│   │   ├── middleware/            # 認証・権限チェック等
│   │   └── db/                    # データベース接続・マイグレーション
│   └── frontend/                  # フロントエンド
│       ├── components/            # UIコンポーネント
│       ├── pages/                 # 画面
│       ├── hooks/                 # カスタムフック
│       └── services/              # API通信
├── tests/                         # テストコード（未実装）
│   ├── unit/                      # 単体テスト
│   ├── integration/               # 結合テスト
│   └── e2e/                       # E2Eテスト
├── CLAUDE.md                      # このファイル（プロジェクト概要）
└── README.md                      # プロジェクトREADME
```

---

## データベース設計概要

システムは以下の5つのテーブルで構成されています。

### テーブル一覧
1. **users（営業マスタ）** - 営業担当者と上長の情報
2. **customers（顧客マスタ）** - 顧客情報
3. **daily_reports（日報）** - 日次報告（Problem/Plan）
4. **visit_records（訪問記録）** - 顧客訪問の記録（1日に複数件）
5. **comments（コメント）** - 上長からのフィードバック

詳細は docs/requirements.md を参照してください。

---

## 技術スタック（推奨）

### バックエンド
- **言語**: Node.js (TypeScript) / Python
- **フレームワーク**: Express.js / NestJS / FastAPI
- **データベース**: PostgreSQL 15.x / MySQL 8.0
- **認証**: JWT (JSON Web Token)
- **ORM**: Prisma / TypeORM / SQLAlchemy

### フロントエンド
- **フレームワーク**: React / Vue.js / Next.js
- **言語**: TypeScript
- **状態管理**: Redux / Zustand / Pinia
- **UIライブラリ**: Material-UI / Ant Design / Tailwind CSS
- **HTTPクライアント**: Axios / Fetch API

### テスト
- **単体テスト**: Jest / Vitest
- **E2Eテスト**: Playwright / Cypress
- **APIテスト**: Postman / REST Client

### インフラ
- **Webサーバー**: Nginx
- **コンテナ**: Docker / Docker Compose
- **CI/CD**: GitHub Actions / GitLab CI

---

## 開発ガイドライン

### 1. ブランチ戦略
- `main`: 本番環境ブランチ
- `develop`: 開発環境ブランチ
- `feature/*`: 機能開発ブランチ
- `bugfix/*`: バグ修正ブランチ

### 2. コミットメッセージ
```
<type>: <subject>

<body>

<footer>
```

**Type:**
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント
- `style`: コードスタイル
- `refactor`: リファクタリング
- `test`: テスト
- `chore`: その他

### 3. コーディング規約
- TypeScript: ESLint + Prettier
- Python: PEP 8 + Black
- コメントは日本語で記載
- 関数・変数名は英語（わかりやすい命名）

### 4. セキュリティ要件
- パスワードは必ずハッシュ化（bcrypt推奨）
- XSS対策: 入力値のエスケープ処理
- SQLインジェクション対策: プリペアドステートメント使用
- CSRF対策: トークン検証
- HTTPS通信必須

### 5. パフォーマンス要件
- 画面表示: 3秒以内
- API応答: 2秒以内（検索API: 5秒以内）
- データベースクエリの最適化（インデックス活用）

---

## API認証フロー

1. **ログイン**: `POST /auth/login` でメール・パスワードを送信
2. **トークン取得**: JWTアクセストークンを受け取る（有効期限: 1時間）
3. **API呼び出し**: `Authorization: Bearer {token}` ヘッダーに含めて送信
4. **ログアウト**: `POST /auth/logout` でトークンを無効化

詳細は docs/api-guide.md を参照してください。

---

## 権限制御

### 役割（Role）
- **staff（一般営業）**: 自分の日報のみ管理可能
- **manager（上長）**: 全日報の閲覧、コメント投稿、営業管理が可能

### 権限マトリックス
| 機能 | 一般営業 | 上長 |
|------|---------|------|
| 自分の日報作成・編集 | ○ | ○ |
| 他人の日報閲覧 | × | ○ |
| コメント投稿 | × | ○ |
| 顧客マスタ管理 | ○ | ○ |
| 営業マスタ管理 | × | ○ |

詳細は docs/screen-design.md および docs/api-guide.md を参照してください。

---

## ビジネスルール

### 日報
- 同じユーザーが同じ日付で複数の日報を作成できない（UNIQUE制約）
- 日報の編集・削除は作成から7日以内のみ可能
- 日報には最低1件の訪問記録が必要
- 日報削除時、関連する訪問記録とコメントもカスケード削除

### コメント
- コメントは上長（role='manager'）のみ投稿可能
- コメントの編集・削除は投稿者のみ可能

### データ制限
- Problem（課題）: 最大5000文字
- Plan（計画）: 最大5000文字
- visit_content（訪問内容）: 最大2000文字
- comment_text（コメント）: 最大2000文字

---

## セットアップ手順（概要）

### 1. 環境準備
```bash
# リポジトリクローン
git clone <repository-url>
cd business-daily-report

# 依存関係インストール
npm install  # または yarn install / pip install -r requirements.txt

# 環境変数設定
cp .env.example .env
# .envファイルを編集（データベース接続情報、JWT秘密鍵など）
```

### 2. データベースセットアップ
```bash
# データベース作成
npm run db:create

# マイグレーション実行
npm run db:migrate

# シードデータ投入（開発環境のみ）
npm run db:seed
```

### 3. 開発サーバー起動
```bash
# バックエンド起動
npm run dev:backend

# フロントエンド起動（別ターミナル）
npm run dev:frontend
```

### 4. テスト実行
```bash
# 全テスト実行
npm run test

# E2Eテスト実行
npm run test:e2e
```

---

## よくある実装タスク

### 日報作成機能の実装
1. docs/screen-design.md のSC-04を参照して画面を実装
2. docs/api-specification.yaml の `POST /reports` を参照してAPIを実装
3. docs/requirements.md のdaily_reportsテーブルとvisit_recordsテーブルを参照してデータモデルを作成
4. docs/test-specification.md のTC-REPORT-001〜TC-REPORT-003を参照してテストを実装

### 権限チェックの実装
1. docs/api-guide.md の「権限制御」セクションを参照
2. ミドルウェアで `role` をチェック
3. 一般営業は自分の日報のみアクセス可能（user_idで比較）
4. docs/test-specification.md のTC-PERM-001〜TC-PERM-003でテスト

### コメント機能の実装
1. docs/screen-design.md のSC-06（コメント投稿部）を参照
2. docs/api-specification.yaml の `POST /reports/{report_id}/comments` を実装
3. 上長のみ投稿可能（role='manager'のチェック）
4. docs/test-specification.md のTC-COMMENT-001〜TC-COMMENT-002でテスト

---

## トラブルシューティング

### 日報の重複エラー
- **原因**: 同じ日付で既に日報が存在
- **解決**: daily_reportsテーブルの(user_id, report_date)のUNIQUE制約を確認
- **参照**: docs/requirements.md の「3.1 エンティティ定義」

### 編集できない（7日経過）
- **原因**: 作成から7日以上経過している
- **解決**: created_atと現在日時を比較するロジックを確認
- **参照**: docs/screen-design.md のSC-05、docs/test-specification.md のTC-REPORT-005

### コメント投稿が403エラー
- **原因**: 一般営業がコメント投稿を試みている
- **解決**: ユーザーのroleが'manager'であることを確認
- **参照**: docs/api-guide.md の「権限マトリックス」

---

## 次のステップ

### 未実装の項目
1. バックエンドAPIの実装
2. フロントエンド画面の実装
3. データベースマイグレーションスクリプト
4. 自動テストの実装
5. Docker環境の構築
6. CI/CDパイプラインの設定

### 推奨される実装順序
1. データベース設計とマイグレーション
2. 認証API（ログイン・ログアウト）
3. 日報API（CRUD）
4. 訪問記録API
5. コメントAPI
6. フロントエンド（画面実装）
7. テストコード
8. デプロイ設定

---

## 参考リンク

- OpenAPI仕様: https://swagger.io/specification/
- JWT認証: https://jwt.io/
- REST API設計: https://restfulapi.net/
- PostgreSQL: https://www.postgresql.org/docs/
- React: https://react.dev/
- TypeScript: https://www.typescriptlang.org/

---

## お問い合わせ

プロジェクトに関する質問や提案は、Issueまたはプルリクエストで受け付けています。

---

**最終更新日**: 2026-01-24
