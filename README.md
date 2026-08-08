# MoguMogu（保育園児の親向け献立自動生成アプリ）

少子化が進む現代社会において、子育て世帯（特に共働き世帯）が抱える「毎日の食事準備」という
時間的・精神的負担を、テクノロジーで軽減することを目的とした Web アプリケーションです。

保育園から配布される**献立表を OCR で読み取り**、園の昼食と食材が重複せず、
**家庭の冷蔵庫の在庫・子どものアレルギー・好き嫌いを考慮した夕食献立を AI が自動提案**します。

## プロジェクトの背景

- 最新（2025 年）の出生数は約 67 万人と過去最少、合計特殊出生率も 1.14 と過去最低
- 子育て世代の 42.5% が「自分の時間が取れない」ことに悩んでいる
- 子どもを持つ家庭は家事・育児に費やす時間が大きく（1 日あたり約 110 分の差）、食事準備は
  保護者にとって大きな負担となる家事の代表格

国が推進する少子化対策・子育て支援（こどもまんなか社会）の方向性に沿い、
「毎日発生する食事準備の負担を軽減することで、子育てしやすい社会づくりに貢献する」ことを目指します。

## 主要機能

| 機能 | 内容 |
|------|------|
| **献立表の OCR 読み取り** | 保育園から配布された献立表（PDF / 画像）をアプリに読み込み、メニュー名を自動でデータ化（スキャン PDF は全ページ画像 OCR にフォールバック） |
| **子ども情報の登録** | 子どもの年齢・アレルギー・好き嫌いをデータベースとして一元管理・編集 |
| **AI 献立自動提案** | 園の昼食・在庫・アレルギー・好き嫌い・前日の夕食を考慮し、レシピ DB から夕食献立を 1〜7 日分自動生成（Gemini / ルールベース） |
| **レシピ表示** | 提案された献立のレシピ（使用食品・作り方）を表示 |
| **買い物リスト生成** | 提案献立に必要な食材から在庫を差し引いた不足食材の買い物リストを自動作成 |
| **フィードバック収集** | ユーザーテスト・学祭アンケート用の評価（1〜5）・コメント投稿 |

## 技術スタック

| レイヤー | 技術 |
|---------|------|
| フロントエンド | Next.js / React / TypeScript |
| バックエンド | FastAPI（Python） |
| データベース | PostgreSQL（本番）/ SQLite（開発） |
| BaaS | Supabase |
| AI | Gemini（OpenAI 互換 API） |
| デプロイ | Vercel |
| 開発環境 | Node.js / Python / GitHub / Figma / ESLint / Prettier |

## 必要環境

| 要件 | バージョン |
|------|-----------|
| Node.js | 18 以上 |
| Python | **3.12**（`backend/.venv` は `py -3.12` で作成） |
| OS | Windows（推奨。起動スクリプトは Windows 向け）|

> 注意: `npm run setup:backend` は `py -3.12` を呼ぶため、Python 3.12（py ランチャー）をインストールしてください。
> 画像 OCR には Gemini の API キーが必要です（後述の「画像 OCR・AI 献立生成を有効にする」を参照）。

## クイックスタート

### 0. 事前準備（git clone 後に初回のみ）

```bash
# 1) フロントエンドの環境変数ファイルを作成（未作成の場合）
cp frontend/.env.example frontend/.env.local
# Windows: copy frontend\.env.example frontend\.env.local

# 2) バックエンドの環境変数ファイル（開発は任意。作らない場合はデフォルトで動作）
#    cp backend/.env.example backend/.env   （Windows: copy backend\.env.example backend\.env）
```

### 1. セットアップ

```bash
npm run setup
```

フロントエンド（npm install）とバックエンド（Python venv 3.12 + pip install）を同時にセットアップします。
Python を複数入れている環境では `.venv` が誤った Python を参照することがあるため、
`backend/.venv/pyvenv.cfg` の `home` が `...\Python312` を指していることを確認してください。

### 2. 開発サーバーを起動

```bash
npm run dev
```

- フロントエンド: http://localhost:3000
- バックエンド API: http://localhost:8000 （Swagger UI: http://localhost:8000/docs）

レシピ検索・レシピ詳細はログイン不要でアクセスできます（バックエンドの読み取り専用 API を公開）。
その他の機能（献立・買い物・フィードバックなど）はログイン後に利用できます。

### 3. 開発環境の注意

- バックエンドの `.venv` は **Python 3.12（標準の py ランチャー）** で作成されます。
  別の Python（例: 画像生成用の複数 Python 環境）が PATH の先頭にある場合、
  `npm run setup:backend` が正しい環境を作れないため、`py -3.12` が使えることを確認してください。
- バックエンド / フロントエンドは個別に起動できます:
  ```bash
  npm run start:backend   # scripts/start-backend.bat（uvicorn をバックグラウンド起動）
  npm run start:frontend  # scripts/start-frontend.bat（Next.js をバックグラウンド起動）
  ```

### 4. 画像 OCR・AI 献立生成を有効にする

デフォルトのインストールでは **デジタル PDF のテキスト抽出**（pypdf）が利用できます。
**画像ファイル（PNG / JPEG）の読み取り** と **AI 献立生成** には Google の
**Gemini（OpenAI 互換 API）** を使います。無料の API キーは
[Aistudio](https://aistudio.google.com) で取得できます（Google アカウント必須）。

1. `backend/.env` に API キーを設定:
   ```bash
   AI_API_KEY=あなたのキー
   AI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
   AI_MODEL=gemini-2.5-flash
   ```
2. スキャン済み PDF を画像化する場合は軽量依存のみ追加:
   ```bash
   cd backend
   .venv\Scripts\pip install -r requirements-ocr.txt
   ```
   （easyocr / PyTorch は不要。API キー未設定でもアプリは動作し、献立生成はルールベース・画像 OCR はエラーになります）

> 注意: 画像を外部（Google）に送信します。機密情報を含む献立表を扱う場合はご注意ください。

## NPM Scripts

| コマンド | 内容 |
|---------|------|
| `npm run setup` | フロント・バック同時セットアップ |
| `npm run dev` | フロント・バック同時起動（開発） |
| `npm run dev:frontend` | フロントエンドのみ起動 |
| `npm run dev:backend` | バックエンドのみ起動 |
| `npm run start:backend` / `npm run start:frontend` | バックグラウンド起動（bat） |
| `npm run build` | フロントエンドのプロダクションビルド |
| `npm run lint` | ESLint 実行 |
| `npm run test` | バックエンドの pytest 実行 |

## テスト

バックエンドの API テストは pytest で実行します（認証・お子様・レシピ・献立生成・買い物リスト・献立表 OCR・セキュリティ・フィードバックの 55 件）。

```bash
npm run test
```

## 本番（デプロイ）時の必須設定

`APP_ENV=production` でバックエンドを起動する場合、起動時に以下を検証し、不備があればエラーで停止します（`backend/app/config.py`）。

| 項目 | 要件 |
|------|------|
| `JWT_SECRET_KEY` | 32 文字以上のランダム値（`.env` で設定。デフォルト値はエラー） |
| `CORS_ORIGINS_RAW` | localhost を含めない（本番オリジンを指定） |
| `DATABASE_URL` | SQLite 禁止（PostgreSQL などの本番 DB を指定） |

`DATABASE_URL` に PostgreSQL を使う場合は `psycopg2-binary` が `backend/requirements.txt` に含まれています（SQLite 開発では未使用）。

設定例は `backend/.env.example` を参照してください。`.env` は git 管理外です。

## セキュリティ対策

| 対策 | 内容 |
|------|------|
| パスワード | bcrypt でハッシュ化。強度要件（8 文字以上・英字と数字を含む）をバックエンドとフロントの両方で検証 |
| JWT | 発行者（iss）・有効期限（exp）を検証。秘密鍵は設定で必須化（本番はデフォルト禁止） |
| レート制限 | ログイン・登録への連続試行を IP ごとに制限（デフォルト 5 回 / 60 秒） |
| 入力検証 | Pydantic / EmailStr による型・長さ・範囲のバリデーション |
| DB アクセス | SQLAlchemy ORM 使用により SQL インジェクションを防止 |
| レシピ公開 | バックエンドの読み取り専用エンドポイントのみ公開（レシピ検索・詳細はログイン不要） |

## プロジェクト構成

```
MoguMogu/
├── package.json              # モノレポ設定（npm workspaces）
├── docs/
│   ├── proposal.md           # 提案書（背景・目的・機能）
│   ├── design.md             # 詳細設計書（アーキテクチャ・API・DB）
│   ├── assignment.md         # タスク割当表・開発スケジュール
│   └── user-manual.md        # ユーザーマニュアル
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI エントリポイント
│   │   ├── config.py         # 環境設定（JWT・AI・レート制限）
│   │   ├── database.py       # DB 接続設定
│   │   ├── middleware.py     # レート制限ミドルウェア
│   │   ├── models.py         # SQLAlchemy モデル
│   │   ├── schemas.py        # Pydantic スキーマ
│   │   ├── security.py       # パスワード・JWT ユーティリティ
│   │   ├── routers/
│   │   │   ├── auth.py       # 認証 API
│   │   │   ├── children.py   # お子様管理 API
│   │   │   ├── menus.py      # 献立表 OCR API
│   │   │   ├── recipes.py    # AI 献立提案 API
│   │   │   ├── recipe_master.py # レシピマスタ CRUD
│   │   │   ├── shopping.py   # 買い物リスト API
│   │   │   └── feedback.py   # フィードバック API
│   │   └── services/
│   │       ├── ocr.py        # OCR（PDF / 画像）
│   │       ├── menu_parser.py # 献立テキスト構造化
│   │       ├── menu_generator.py # AI 献立生成
│   │       ├── shopping_list.py # 買い物リスト集計
│   │       └── seed_data.py  # レシピシード 29 件
│   ├── app/main.py           # FastAPI エントリ（起動時に seed 実行）
│   ├── app/seed.py           # レシピシード投入
│   ├── tests/                # pytest テスト
│   ├── requirements.txt
│   ├── requirements-ocr.txt  # pypdfium2（スキャン PDF の画像化のみ）
│   └── requirements-dev.txt  # pytest 等
└── frontend/
    ├── src/
    │   ├── app/              # Next.js App Router
    │   │   ├── layout.tsx
    │   │   ├── page.tsx      # トップページ
    │   │   ├── login/        # ログイン画面
    │   │   ├── register/     # 新規登録画面
    │   │   ├── dashboard/    # お子様・プロフィール管理
    │   │   ├── meal-plan/    # AI 献立生成画面
    │   │   ├── menus/        # 献立表 OCR 取り込み
    │   │   ├── recipe-search/ # レシピ検索（ログイン不要）
    │   │   ├── recipe-master/[id] # レシピ詳細（ログイン不要）
    │   │   ├── recipes/      # 提案献立一覧
    │   │   ├── shopping/     # 買い物リスト・冷蔵庫
    │   │   └── feedback/     # フィードバック
    │   ├── components/       # 共通コンポーネント（AppNav 等）
    │   └── lib/              # API クライアント等
    ├── package.json
    └── next.config.js
```

## ドキュメント

- [提案書](./docs/proposal.md) — プロジェクトの背景・目的・機能・市場分析
- [詳細設計書](./docs/design.md) — アーキテクチャ・API・データベース設計
- [タスク割当表](./docs/assignment.md) — メンバー別タスク・開発スケジュール
- [ユーザーマニュアル](./docs/user-manual.md) — 画面ごとの使い方ガイド

## ライセンス

MIT
