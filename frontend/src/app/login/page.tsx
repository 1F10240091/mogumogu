"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await api.login(email, password);
      localStorage.setItem("token", res.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "ログインに失敗しました");
    }
  };

  return (
    <main className="auth-page">
      <div className="auth-card">
        <Link
          href="/"
          style={{
            display: "block",
            textAlign: "center",
            fontSize: 22,
            fontWeight: "bold",
            color: "var(--color-primary-dark)",
            marginBottom: 16,
          }}
        >
          もぐもぐ
        </Link>
        <h1 className="auth-card__title">ログイン</h1>
        <p className="auth-card__subtitle">もぐもぐで毎日の献立づくりを楽に</p>
        <form
          onSubmit={handleSubmit}
          style={{ display: "flex", flexDirection: "column", gap: 16 }}
        >
          <input
            type="email"
            placeholder="メールアドレス"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="input"
          />
          <input
            type="password"
            placeholder="パスワード"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="input"
          />
          {error && <div className="alert alert--error">{error}</div>}
          <button type="submit" className="button button--full">
            ログイン
          </button>
        </form>
        <p className="auth-card__footer">
          アカウントをお持ちでない方は <Link href="/register">新規登録</Link>
        </p>
      </div>
    </main>
  );
}
