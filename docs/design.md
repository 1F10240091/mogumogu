# 詳細設計書

## 1. アーキテクチャ

```
┌──────────────┐    HTTP    ┌──────────────┐          ┌──────────────┐
│   Frontend   │ ─────────▶ │   Backend    │ ───────▶ │      AI      │
│ (Next.js/TS) │ ◀───────── │  (FastAPI)   │ ◀─────── │ (Xiaomi MiMo)│
└──────────────┘   REST     └──────┬───────┘   API    └──────────────┘
                                   │
                            ┌──────▼───────┐
                            │  Database    │
                            │(Supabase/PostgreSQL)│
                            └──────────────┘
```

- フロントエンドは Next.js + TypeScript。App Router によるページ構成。
- バックエンドは FastAPI（Python）による REST API。
- AI（Xiaomi MiMo）をバックエンドから呼び出し、献立を自動生成する。
- データベースは開発時 SQLite、本番は Supabase（PostgreSQL）。

## 2. API 設計

ベース URL: `/api/v1`

### 認証

| メソッド | パス | 説明 |
|---------|------|------|
| POST | `/api/v1/auth/register` | 新規ユーザー登録 |
| POST | `/api/v1/auth/login` | ログイン（JWT 発行） |
| GET | `/api/v1/auth/me` | ログインユーザー情報取得 |

### お子様管理

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/api/v1/children` | お子様一覧取得 |
| POST | `/api/v1/children` | お子様登録 |
| GET | `/api/v1/children/{id}` | お子様詳細取得 |
| PUT | `/api/v1/children/{id}` | お子様情報更新 |
| DELETE | `/api/v1/children/{id}` | お子様削除 |

### 献立表（OCR）

| メソッド | パス | 説明 |
|---------|------|------|
| POST | `/api/v1/menus/upload` | 献立表 PDF/画像をアップロードし OCR 実行 |
| GET | `/api/v1/menus` | 取り込み済み献立一覧 |
| GET | `/api/v1/menus/{id}` | 献立詳細 |

### AI 献立提案

| メソッド | パス | 説明 |
|---------|------|------|
| POST | `/api/v1/recipes/generate` | 献立自動生成（保育園食・在庫・アレルギー・好みを考慮） |
| GET | `/api/v1/recipes` | 提案済み献立一覧 |
| GET | `/api/v1/recipes/{id}` | レシピ詳細 |

### 買い物リスト

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/api/v1/shopping/list` | 買い物リスト取得 |
| POST | `/api/v1/shopping/generate` | 不足食材リスト生成 |
| PATCH | `/api/v1/shopping/{item_id}` | 買い物リスト項目更新 |

## 3. データベース設計

### users（ユーザー）

| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | 主キー |
| email | TEXT | ログインID（ユニーク） |
| hashed_password | TEXT | パスワードハッシュ |
| display_name | TEXT | 表示名 |
| created_at | TIMESTAMP | 作成日時 |

### children（お子様）

| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | 主キー |
| user_id | UUID | 外部キー（users） |
| name | TEXT | お子様名 |
| birth_date | DATE | 生年月日 |
| gender | TEXT | 性別 |
| created_at | TIMESTAMP | 作成日時 |

### allergies（アレルギー）

| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | 主キー |
| child_id | UUID | 外部キー（children） |
| ingredient | TEXT | アレルギー食材 |

### preferences（好き嫌い）

| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | 主キー |
| child_id | UUID | 外部キー（children） |
| ingredient | TEXT | 対象食材 |
| mode | TEXT | `exclude`（除外）/ `improve`（改善優先） |

### nursery_menus（保育園献立）

| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | 主キー |
| user_id | UUID | 外部キー（users） |
| date | DATE | 日付 |
| menu_text | TEXT | OCR で取得した献立テキスト |
| ingredients | JSON | 食材リスト |
| created_at | TIMESTAMP | 作成日時 |

### inventory_items（冷蔵庫の在庫）

| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | 主キー |
| user_id | UUID | 外部キー（users） |
| name | TEXT | 食材名 |
| quantity | TEXT | 数量 |
| updated_at | TIMESTAMP | 更新日時 |

### suggested_meals（提案献立）

| カラム | 型 | 説明 |
|--------|-----|------|
| id | UUID | 主キー |
| user_id | UUID | 外部キー（users） |
| date | DATE | 対象日 |
| menu_text | TEXT | 提案内容 |
| ingredients | JSON | 使用食材 |
| created_at | TIMESTAMP | 作成日時 |

## 4. AI 献立生成ロジック（設計）

1. 指定日の保育園献立（nursery_menus）を取得
2. 対象児のアレルギー（allergies）・好き嫌い（preferences）を取得
3. 冷蔵庫の在庫（inventory_items）を取得
4. 上記をプロンプトに組み込み、Xiaomi MiMo に夕食献立を生成させる
5. 制約：
   - 園の昼食と使用食材が重複しない
   - アレルギー食材を除外する
   - 「改善優先」食材は少量から段階的に取り入れる
   - 在庫を優先的に活用し、不足食材のみ買い物リストに追加する
