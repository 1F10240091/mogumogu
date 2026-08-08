"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import AppNav from "@/components/AppNav";
import RequireAuth from "@/components/RequireAuth";
import { api, type NurseryMenu } from "@/lib/api";

export default function MenusPage() {
  const [menus, setMenus] = useState<NurseryMenu[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadMenus = () => {
    api
      .listMenus()
      .then(setMenus)
      .catch((err) =>
        setError(
          err instanceof Error ? err.message : "献立表の取得に失敗しました",
        ),
      )
      .finally(() => setLoading(false));
  };

  useEffect(loadMenus, []);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setError(null);
    try {
      await api.uploadMenu(file);
      loadMenus();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "アップロードに失敗しました",
      );
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  return (
    <RequireAuth>
      <main className="main">
        <AppNav />
        <div className="container" style={{ paddingBottom: 80 }}>
          <div className="page-header">
            <h1 className="page-header__title">献立表の取り込み</h1>
            <p className="page-header__subtitle">
              保育園から配布された献立表を読み取り、デジタル化します。
            </p>
          </div>
          <div className="card">
            <p className="card__text">
              保育園から配布された献立表（PDF
              または画像）をアップロードしてください。
            </p>
            <label
              className="button"
              style={{ display: "inline-block", cursor: "pointer" }}
            >
              {uploading ? "読み取り中..." : "献立表をアップロード"}
              <input
                type="file"
                accept=".pdf,image/png,image/jpeg,image/webp"
                onChange={handleUpload}
                hidden
              />
            </label>
            {error && <div className="alert alert--error">{error}</div>}
          </div>

          {loading ? (
            <div className="loading">読み込み中...</div>
          ) : menus.length === 0 ? (
            <div className="card">
              <p className="card__text">
                まだ取り込んだ献立表がありません。上のボタンからアップロードしてください。
              </p>
            </div>
          ) : (
            menus.map((menu) => (
              <div className="card" key={menu.id}>
                <h2>{menu.date}</h2>
                <pre
                  style={{
                    whiteSpace: "pre-wrap",
                    fontFamily: "inherit",
                    margin: 0,
                  }}
                >
                  {menu.menu_text}
                </pre>
              </div>
            ))
          )}
          <div className="action-links">
            <Link href="/meal-plan" className="button">
              AI 献立提案へ進む
            </Link>
          </div>
        </div>
      </main>
    </RequireAuth>
  );
}
