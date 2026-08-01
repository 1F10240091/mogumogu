# Hoiku-Recipe（保育園児の親向け献立自動生成アプリ）

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
| **AI 献立自動提案** | 園の昼食・在庫・アレルギー・好き嫌い・前日の夕食を考慮し、レシピ DB から夕食献立を 1〜7 日分自動生成（Xiaomi MiMo / ルールベース） |
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
| AI | Xiaomi MiMo |
| デプロイ | Vercel |
| 開発環境 | Node.js / Python / GitHub / Figma / ESLint / Prettier |

## 必要環境

| 要件 | バージョン |
|------|-----------|
| Node.js | 18 以上 |
| Python | 3.10 以上 |
| OS | Windows / macOS / Linux |

## クイックスタート

### 1. セットアップ

```bash
npm run setup
```

フロントエンド（npm install）とバックエンド（Python venv + pip install）を同時にセットアップします。

### 2. 開発サーバーを起動

```bash
npm run dev
```

- フロントエンド: http://localhost:3000
- バックエンド API: http://localhost:8000 （Swagger UI: http://localhost:8000/docs）

## デモモード（バックエンド不要）

バックエンドを起動せずに、フロントエンドだけで全機能を試すことができます。
デモモードではモック API が動作し、データはブラウザの localStorage に保存されます。

```bash
# frontend/.env.local に追記
NEXT_PUBLIC_DEMO_MODE=true
```

ログイン画面の「デモを試す」ボタンから、ワンクリックでデモログインできます
（あらかじめサンプルデータが用意されています）。デモモード中はどのメールアドレス・
パスワードでもログインできます。

> デモモードは評価・デモ用途のためのものです。本番利用では使用しないでください。

## NPM Scripts

| コマンド | 内容 |
|---------|------|
| `npm run setup` | フロント・バック同時セットアップ |
| `npm run dev` | フロント・バック同時起動 |
| `npm run dev:frontend` | フロントエンドのみ起動 |
| `npm run dev:backend` | バックエンドのみ起動 |
| `npm run build` | フロントエンドのプロダクションビルド |
| `npm run lint` | ESLint 実行 |

## テスト

バックエンドの API テストは pytest で実行します（認証・お子様・レシピ・献立生成・買い物リスト・献立表 OCR・セキュリティ・フィードバックの 40 件）。

```bash
cd backend
pip install -r requirements-dev.txt
python -m pytest tests -v
```

## セキュリティ対策

| 対策 | 内容 |
|------|------|
| パスワード | bcrypt でハッシュ化。強度要件（8 文字以上・英字と数字を含む）をバックエンドとフロントの両方で検証 |
| JWT | 発行者（iss）・有効期限（exp）を検証。秘密鍵は環境変数で設定 |
| レート制限 | ログイン・登録への連続試行を IP ごとに制限（デフォルト 5 回 / 60 秒） |
| 入力検証 | Pydantic / EmailStr による型・長さ・範囲のバリデーション |
| DB アクセス | SQLAlchemy ORM 使用により SQL インジェクションを防止 |

## プロジェクト構成

```
hoiku-recipe/
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
│   │       └── seed_data.py  # レシピシード 23 件
│   ├── tests/                # pytest テスト
│   ├── requirements.txt
│   ├── requirements-ocr.txt  # easyocr 等（画像 OCR のみ）
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
