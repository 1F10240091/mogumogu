"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const passwordPattern = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/;
    if (!passwordPattern.test(password)) {
      setError(
        "パスワードは8文字以上で、英字と数字をそれぞれ1文字以上含めてください",
      );
      return;
    }
    try {
      const res = await api.register(email, password, name);
      localStorage.setItem("token", res.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "登録に失敗しました");
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
        <h1 className="auth-card__title">新規登録</h1>
        <p className="auth-card__subtitle">
          アカウントを作成して献立づくりを始めましょう
        </p>
        <form
          onSubmit={handleSubmit}
          style={{ display: "flex", flexDirection: "column", gap: 16 }}
        >
          <input
            type="text"
            placeholder="名前（任意）"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="input"
          />
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
          <p className="form-field__hint">
            パスワードは8文字以上で、英字と数字をそれぞれ1文字以上含めてください。
          </p>
          {error && <div className="alert alert--error">{error}</div>}
          <button type="submit" className="button button--full">
            登録する
          </button>
        </form>
        <p className="auth-card__footer">
          すでにアカウントをお持ちの方は <Link href="/login">ログイン</Link>
        </p>
      </div>
    </main>
  );
}
