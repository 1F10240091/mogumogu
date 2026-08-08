"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, type User } from "@/lib/api";

// トークン検証＋未ログイン時に /login へリダイレクトするガード。
// レシピ検索・レシピ詳細はログイン不要のため、このガードを使わない。
export default function RequireAuth({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [checking, setChecking] = useState(true);
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    api
      .me()
      .then((me) => {
        setUser(me);
        setChecking(false);
      })
      .catch(() => {
        router.replace("/login");
      });
  }, [router]);

  if (checking) {
    return (
      <div className="page-header">
        <div className="loading">読み込み中...</div>
      </div>
    );
  }

  return <>{user ? children : null}</>;
}

export function useCurrentUser() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .me()
      .then((me) => setUser(me))
      .finally(() => setLoading(false));
  }, []);

  return { user, loading };
}