# 営業日報システム API ガイド

## 概要

このドキュメントは営業日報システムのAPI仕様の補足ガイドです。
詳細なAPI仕様は [api-specification.yaml](api-specification.yaml) を参照してください。

## API仕様の閲覧方法

OpenAPI仕様書は以下のツールで閲覧できます:

1. **Swagger UI**
   - https://editor.swagger.io/ にアクセス
   - `api-specification.yaml` の内容を貼り付け

2. **VSCode拡張機能**
   - `OpenAPI (Swagger) Editor` 拡張機能をインストール
   - `api-specification.yaml` を開く

3. **Redoc**
   - オンラインビューアー: https://redocly.github.io/redoc/

---

## エンドポイント一覧

### 認証
| メソッド | エンドポイント | 説明 | 権限 |
|---------|---------------|------|------|
| POST | `/auth/login` | ログイン | 全ユーザー |
| POST | `/auth/logout` | ログアウト | 認証済み |
| GET | `/auth/me` | ログインユーザー情報取得 | 認証済み |

### 日報
| メソッド | エンドポイント | 説明 | 権限 |
|---------|---------------|------|------|
| GET | `/reports` | 日報一覧取得 | 認証済み |
| POST | `/reports` | 日報作成 | 一般営業 |
| GET | `/reports/{report_id}` | 日報詳細取得 | 認証済み |
| PUT | `/reports/{report_id}` | 日報更新 | 作成者のみ |
| DELETE | `/reports/{report_id}` | 日報削除 | 作成者のみ |

### 訪問記録
| メソッド | エンドポイント | 説明 | 権限 |
|---------|---------------|------|------|
| POST | `/reports/{report_id}/visits` | 訪問記録追加 | 作成者のみ |
| PUT | `/visits/{visit_id}` | 訪問記録更新 | 作成者のみ |
| DELETE | `/visits/{visit_id}` | 訪問記録削除 | 作成者のみ |

### コメント
| メソッド | エンドポイント | 説明 | 権限 |
|---------|---------------|------|------|
| GET | `/reports/{report_id}/comments` | コメント一覧取得 | 認証済み |
| POST | `/reports/{report_id}/comments` | コメント投稿 | 上長のみ |
| PUT | `/comments/{comment_id}` | コメント更新 | 投稿者のみ |
| DELETE | `/comments/{comment_id}` | コメント削除 | 投稿者のみ |

### 顧客
| メソッド | エンドポイント | 説明 | 権限 |
|---------|---------------|------|------|
| GET | `/customers` | 顧客一覧取得 | 認証済み |
| POST | `/customers` | 顧客登録 | 認証済み |
| GET | `/customers/{customer_id}` | 顧客詳細取得 | 認証済み |
| PUT | `/customers/{customer_id}` | 顧客更新 | 認証済み |
| DELETE | `/customers/{customer_id}` | 顧客削除 | 認証済み |

### 営業
| メソッド | エンドポイント | 説明 | 権限 |
|---------|---------------|------|------|
| GET | `/users` | 営業一覧取得 | 上長のみ |
| POST | `/users` | 営業登録 | 上長のみ |
| GET | `/users/{user_id}` | 営業詳細取得 | 上長のみ |
| PUT | `/users/{user_id}` | 営業更新 | 上長のみ |
| DELETE | `/users/{user_id}` | 営業削除 | 上長のみ |

---

## 認証

### 認証方式
JWT（JSON Web Token）を使用したBearer認証

### 認証フロー

1. **ログイン**
```bash
curl -X POST https://api.example.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tanaka@example.com",
    "password": "password123"
  }'
```

レスポンス:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "user_id": 1,
    "name": "田中花子",
    "email": "tanaka@example.com",
    "role": "staff"
  }
}
```

2. **認証が必要なAPIの呼び出し**
```bash
curl -X GET https://api.example.com/v1/reports \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

3. **ログアウト**
```bash
curl -X POST https://api.example.com/v1/auth/logout \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## 使用例

### 日報作成の完全フロー

#### 1. ログイン
```bash
POST /auth/login
{
  "email": "tanaka@example.com",
  "password": "password123"
}
```

#### 2. 顧客一覧を取得（訪問先を選ぶため）
```bash
GET /customers?company_name=サンプル
Authorization: Bearer {token}
```

#### 3. 日報を作成
```bash
POST /reports
Authorization: Bearer {token}
Content-Type: application/json

{
  "report_date": "2026-01-24",
  "problem": "新規顧客の開拓が難航している",
  "plan": "既存顧客へのフォローアップを強化する",
  "visit_records": [
    {
      "customer_id": 1,
      "visit_content": "新製品の提案を実施。来月デモを予定"
    },
    {
      "customer_id": 2,
      "visit_content": "既存契約の更新について打ち合わせ"
    }
  ]
}
```

#### 4. 上長がコメントを投稿
```bash
POST /reports/1/comments
Authorization: Bearer {manager_token}
Content-Type: application/json

{
  "comment_text": "新規顧客開拓について、来週ミーティングしましょう"
}
```

---

## ページネーション

一覧取得APIはページネーションをサポートしています。

### リクエストパラメータ
- `page`: ページ番号（デフォルト: 1）
- `per_page`: 1ページあたりの件数（デフォルト: 20、最大: 100）

### リクエスト例
```bash
GET /reports?page=2&per_page=50
Authorization: Bearer {token}
```

### レスポンス例
```json
{
  "data": [
    {
      "report_id": 21,
      "user_name": "田中花子",
      "report_date": "2026-01-23",
      ...
    }
  ],
  "pagination": {
    "current_page": 2,
    "per_page": 50,
    "total": 150,
    "total_pages": 3
  }
}
```

---

## エラーハンドリング

### エラーレスポンスの形式
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力値が不正です",
    "details": [
      {
        "field": "email",
        "message": "メールアドレスの形式が不正です"
      }
    ]
  }
}
```

### HTTPステータスコード

| コード | 説明 |
|--------|------|
| 200 | 成功 |
| 201 | 作成成功 |
| 204 | 削除成功（レスポンスボディなし） |
| 400 | リクエストが不正 |
| 401 | 認証エラー |
| 403 | 権限エラー |
| 404 | リソースが見つからない |
| 500 | サーバーエラー |

### エラーコード一覧

| コード | 説明 |
|--------|------|
| VALIDATION_ERROR | バリデーションエラー |
| UNAUTHORIZED | 認証エラー |
| FORBIDDEN | 権限エラー |
| NOT_FOUND | リソースが見つからない |
| DUPLICATE_ERROR | 重複エラー（例: 同じ日付の日報が既に存在） |
| EDIT_PERIOD_EXPIRED | 編集期限切れ（7日経過） |
| INTERNAL_ERROR | サーバー内部エラー |

---

## 権限制御

### 役割（Role）

| 役割 | 値 | 説明 |
|------|-----|------|
| 一般営業 | staff | 日報の作成・編集、顧客管理 |
| 上長 | manager | 全日報の閲覧、コメント投稿、営業管理 |

### 権限マトリックス

| 機能 | 一般営業 | 上長 |
|------|---------|------|
| 自分の日報作成・編集 | ○ | ○ |
| 自分の日報削除 | ○（7日以内） | ○（7日以内） |
| 他人の日報閲覧 | × | ○ |
| 日報へのコメント投稿 | × | ○ |
| 顧客マスタ管理 | ○ | ○ |
| 営業マスタ管理 | × | ○ |

---

## ビジネスルール

### 日報
- 同じユーザーが同じ日付で複数の日報を作成することはできない
- 日報の編集・削除は作成から7日以内のみ可能
- 日報には最低1件の訪問記録が必要

### 訪問記録
- 訪問記録の順序は `visit_order` フィールドで管理
- 日報が削除されると、関連する訪問記録も削除される（CASCADE）

### コメント
- コメントは上長（role='manager'）のみ投稿可能
- 日報が削除されると、関連するコメントも削除される（CASCADE）

---

## データ制限

### 文字数制限

| フィールド | 最大文字数 |
|-----------|----------|
| problem（課題） | 5000文字 |
| plan（計画） | 5000文字 |
| visit_content（訪問内容） | 2000文字 |
| comment_text（コメント） | 2000文字 |
| company_name（会社名） | 255文字 |
| name（氏名） | 100文字 |
| address（住所） | 500文字 |

### API制限
- 1ページあたりの最大取得件数: 100件
- リクエストレート制限: 未定（将来的に実装予定）

---

## テスト用データ

### テストユーザー（開発環境のみ）

#### 一般営業
```
Email: staff@example.com
Password: password123
Role: staff
```

#### 上長
```
Email: manager@example.com
Password: password123
Role: manager
```

### テスト顧客
```json
{
  "customer_id": 1,
  "company_name": "株式会社テスト",
  "contact_person": "テスト太郎",
  "phone": "03-0000-0000",
  "email": "test@test.co.jp"
}
```

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.0.0 | 2026-01-24 | 初版リリース |

---

## お問い合わせ

API仕様に関する質問や不明点は以下までお問い合わせください。

- Email: support@example.com
- GitHub Issues: （リポジトリURL）
