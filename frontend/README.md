# フロントエンド（Next.js + TypeScript）

保育園児の親向け献立自動生成アプリのフロントエンド。

## 開発

```bash
npm install
npm run dev
```

http://localhost:3000

## ページ構成

| パス | 内容 |
|------|------|
| `/` | トップページ（機能紹介） |
| `/login` | ログイン画面 |
| `/register` | 新規登録画面 |
| `/dashboard` | お子様管理ダッシュボード |
| `/meal-plan` | 献立作成画面 |
| `/recipes` | レシピ・買い物リスト画面 |

## API プロキシ

`next.config.js` の rewrite により、`/api/v1/*` へのリクエストはバックエンド
（デフォルト http://localhost:8000）にプロキシされます。

プロキシ先を変更する場合は `NEXT_PUBLIC_API_URL` 環境変数を設定してください。
