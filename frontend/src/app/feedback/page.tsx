"use client";

import { useState } from "react";
import Link from "next/link";
import AppNav from "@/components/AppNav";
import RequireAuth from "@/components/RequireAuth";
import { api } from "@/lib/api";

const RATINGS = [1, 2, 3, 4, 5];

export default function FeedbackPage() {
  const [rating, setRating] = useState<number | null>(null);
  const [comment, setComment] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    setError(null);
    if (rating === null && !comment.trim()) {
      setError("評価またはコメントを入力してください");
      return;
    }
    try {
      await api.submitFeedback(rating, comment);
      setSubmitted(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "送信に失敗しました");
    }
  };

  return (
    <RequireAuth>
      <main className="main">
      <AppNav />
      <div className="container" style={{ paddingBottom: 80 }}>
        <div className="page-header">
          <h1 className="page-header__title">フィードバック</h1>
          <p className="page-header__subtitle">
            アプリの使い勝手や改善してほしい点を教えてください。今後の開発に活かします。
          </p>
        </div>
        {submitted ? (
          <div className="card">
            <p>ご協力ありがとうございました！</p>
            <div className="action-links">
              <Link href="/dashboard" className="button">
                ダッシュボードへ戻る
              </Link>
            </div>
          </div>
        ) : (
          <div className="card">
            <p className="form-field__label">満足度（1〜5）</p>
            <div className="rating" role="group" aria-label="満足度">
              {RATINGS.map((r) => (
                <button
                  key={r}
                  onClick={() => setRating(r)}
                  aria-pressed={rating === r}
                  className={`rating__button${rating === r ? " rating__button--active" : ""}`}
                >
                  {r}
                </button>
              ))}
            </div>
            <label className="form-field">
              <span className="form-field__label">ご意見・ご要望</span>
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                rows={4}
                className="textarea"
              />
            </label>
            {error && <div className="alert alert--error">{error}</div>}
            <button className="button" onClick={handleSubmit}>
              送信する
            </button>
          </div>
        )}
      </div>
      </main>
    </RequireAuth>
  );
}
