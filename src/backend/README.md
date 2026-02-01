# 営業日報システム - バックエンド

FastAPIを使用した営業日報システムのバックエンドAPI

## 技術スタック

- **言語**: Python 3.11+
- **フレームワーク**: FastAPI
- **データベース**: PostgreSQL 15.x
- **ORM**: SQLAlchemy 2.0
- **認証**: JWT (python-jose)
- **テスト**: pytest
- **その他**: Pydantic, Alembic

## プロジェクト構造

```
src/backend/
├── api/              # APIエンドポイント（ルーター）
├── models/           # SQLAlchemyモデル（データベース）
├── schemas/          # Pydanticスキーマ（リクエスト/レスポンス）
├── services/         # ビジネスロジック
├── middleware/       # ミドルウェア（認証、エラーハンドリング等）
├── db/               # データベース接続・セッション管理
├── tests/            # テストコード
├── config.py         # 設定管理
├── logger.py         # ロギング設定
├── utils.py          # ユーティリティ関数
├── main.py           # エントリーポイント
├── requirements.txt  # 本番依存パッケージ
└── requirements-dev.txt  # 開発依存パッケージ
```

## セットアップ

### 1. 仮想環境の作成と有効化

```bash
# Python仮想環境を作成
python -m venv venv

# 仮想環境を有効化
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 2. 依存パッケージのインストール

```bash
# 本番環境用パッケージ
pip install -r requirements.txt

# 開発環境用パッケージ（テスト、コード品質ツール等）
pip install -r requirements-dev.txt
```

### 3. 環境変数の設定

```bash
# プロジェクトルートで.envファイルを作成
cp ../../.env.example ../../.env

# .envファイルを編集して設定を変更
# 特に以下の項目を確認：
# - DATABASE_URL: データベース接続情報
# - SECRET_KEY: JWT署名用の秘密鍵（本番環境では必ず変更）
```

### 4. データベースのセットアップ

```bash
# PostgreSQLが起動していることを確認

# データベースの作成（初回のみ）
# 注: Alembicマイグレーションを使用する場合は不要
# python -c "from db.database import init_db; init_db()"

# Alembicマイグレーション（推奨）
alembic upgrade head
```

## 起動方法

### 開発サーバーの起動

```bash
# uvicornで起動（ホットリロード有効）
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# または
python main.py
```

### Dockerで起動

```bash
# プロジェクトルートで実行
cd ../..
docker-compose up backend
```

## API仕様の確認

サーバー起動後、以下のURLでAPI仕様を確認できます。

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## テスト

### 全テストの実行

```bash
pytest
```

### カバレッジ付きテスト

```bash
pytest --cov=. --cov-report=html
```

### 特定のマーカーでフィルタリング

```bash
# 単体テストのみ実行
pytest -m unit

# APIテストのみ実行
pytest -m api

# データベーステストを除外
pytest -m "not db"
```

### テストの詳細出力

```bash
pytest -v -s
```

## コード品質

### フォーマット

```bash
# Blackでコードフォーマット
black .

# isortでインポート順序を整理
isort .
```

### リンター

```bash
# flake8でコードチェック
flake8 .

# mypyで型チェック
mypy .
```

## 開発ガイドライン

### コーディング規約

- **コメント**: 日本語で記載
- **関数・変数名**: 英語（わかりやすい命名）
- **Pythonスタイル**: PEP 8準拠
- **型ヒント**: 可能な限り使用

### ディレクトリの役割

- **api/**: FastAPIのルーター定義。エンドポイントごとにファイルを分割
- **models/**: SQLAlchemyモデル。データベーステーブルと1対1対応
- **schemas/**: Pydanticスキーマ。リクエスト/レスポンスの型定義
- **services/**: ビジネスロジック。データベース操作やビジネスルールを実装
- **middleware/**: 認証、エラーハンドリング等の横断的関心事
- **db/**: データベース接続、セッション管理

### エラーハンドリング

カスタム例外を使用してエラーを統一的に処理：

```python
from middleware.errors import NotFoundException, ForbiddenException

# リソースが見つからない場合
raise NotFoundException("日報が見つかりません")

# 権限エラー
raise ForbiddenException("この操作を実行する権限がありません")
```

### ロギング

```python
from logger import app_logger

app_logger.info("処理を開始します")
app_logger.error(f"エラーが発生しました: {e}")
```

## トラブルシューティング

### データベース接続エラー

```bash
# PostgreSQLが起動しているか確認
docker-compose ps

# DATABASE_URLが正しいか確認
echo $DATABASE_URL

# データベースに接続できるかテスト
psql -h localhost -U postgres -d daily_report
```

### インポートエラー

```bash
# 仮想環境が有効化されているか確認
which python

# パッケージが正しくインストールされているか確認
pip list

# 再インストール
pip install -r requirements.txt --force-reinstall
```

### テストエラー

```bash
# テスト用データベースをクリーンアップ
rm -f test.db

# pytestキャッシュをクリア
pytest --cache-clear

# 詳細ログを出力
pytest -v -s --log-cli-level=DEBUG
```

## その他のコマンド

### データベースマイグレーション

```bash
# マイグレーションファイルの作成
alembic revision --autogenerate -m "説明"

# マイグレーションの適用
alembic upgrade head

# マイグレーションのロールバック
alembic downgrade -1
```

### パッケージの更新

```bash
# 依存パッケージの更新
pip install --upgrade -r requirements.txt

# requirements.txtの更新
pip freeze > requirements.txt
```

## 参考リンク

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [SQLAlchemy公式ドキュメント](https://docs.sqlalchemy.org/)
- [Pydantic公式ドキュメント](https://docs.pydantic.dev/)
- [pytest公式ドキュメント](https://docs.pytest.org/)
