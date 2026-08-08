"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import AppNav from "@/components/AppNav";
import SearchBar from "@/components/SearchBar";
import RecipeList from "@/components/RecipeList";
import { api, type RecipeSearchResponse } from "@/lib/api";

function RecipeSearchInner() {
  const searchParams = useSearchParams();
  const [result, setResult] = useState<RecipeSearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    const params = {
      keyword: searchParams.get("keyword") ?? undefined,
      meal_type: searchParams.get("meal_type") ?? undefined,
      ingredient: searchParams.get("ingredient") ?? undefined,
      max_cook_time: searchParams.get("max_cook_time")
        ? Number(searchParams.get("max_cook_time"))
        : undefined,
      page: searchParams.get("page") ? Number(searchParams.get("page")) : 1,
      per_page: 12,
    };

    api
      .searchRecipes(params)
      .then((res) => {
        if (!cancelled) setResult(res);
      })
      .catch((e: unknown) => {
        if (!cancelled)
          setError(e instanceof Error ? e.message : "検索に失敗しました");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [searchParams]);

  return (
    <main className="main">
      <AppNav />
      <div className="container" style={{ paddingBottom: 80 }}>
        <div className="page-header">
          <h1 className="page-header__title">レシピ検索</h1>
          <p className="page-header__subtitle">
            キーワード・カテゴリ・材料・調理時間から保育園向けレシピを探せます。
          </p>
        </div>
        <SearchBar
          initial={{
            keyword: searchParams.get("keyword") ?? undefined,
            meal_type: searchParams.get("meal_type") ?? undefined,
            ingredient: searchParams.get("ingredient") ?? undefined,
            max_cook_time: searchParams.get("max_cook_time")
              ? Number(searchParams.get("max_cook_time"))
              : undefined,
          }}
        />
        {error && (
          <div className="card" role="alert">
            <p>{error}</p>
          </div>
        )}
        {loading && (
          <div className="card">
            <p>読み込み中...</p>
          </div>
        )}
        {result && !loading && <RecipeList result={result} />}
      </div>
    </main>
  );
}

export default function RecipeSearchPage() {
  return (
    <Suspense fallback={null}>
      <RecipeSearchInner />
    </Suspense>
  );
}
