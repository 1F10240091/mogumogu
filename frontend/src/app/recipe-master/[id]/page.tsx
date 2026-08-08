"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import AppNav from "@/components/AppNav";
import { api, type Recipe } from "@/lib/api";

const MEAL_TYPE_LABELS: Record<string, string> = {
  main: "主菜",
  side: "副菜",
  soup: "汁物",
  staple: "主食",
};

export default function RecipeDetailPage({
  params,
}: {
  params: { id: string };
}) {
  const [recipe, setRecipe] = useState<Recipe | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getRecipe(params.id)
      .then(setRecipe)
      .catch((e: unknown) =>
        setError(e instanceof Error ? e.message : "レシピの取得に失敗しました"),
      )
      .finally(() => setLoading(false));
  }, [params.id]);

  return (
    <main className="main">
      <AppNav />
      <div className="container" style={{ paddingBottom: 80 }}>
        <div className="page-header">
          <p style={{ marginBottom: 16 }}>
            <Link
              href="/recipe-search"
              style={{ color: "var(--color-primary-dark)" }}
            >
              ← レシピ検索に戻る
            </Link>
          </p>
        </div>

        {loading && (
          <div className="card">
            <p>読み込み中...</p>
          </div>
        )}

        {error && (
          <div className="card" role="alert">
            <p>{error}</p>
          </div>
        )}

        {recipe && !loading && (
          <article className="card">
            <header style={{ marginBottom: 16 }}>
              <span className="recipe-card__badge">
                {MEAL_TYPE_LABELS[recipe.meal_type] ?? recipe.meal_type}
              </span>
              {recipe.cook_time_minutes != null && (
                <span className="recipe-card__time" style={{ marginLeft: 8 }}>
                  {recipe.cook_time_minutes}分
                </span>
              )}
              <h1 style={{ marginTop: 8 }}>{recipe.name}</h1>
            </header>

            <h2>材料</h2>
            <ul className="recipe-detail__ingredients">
              {recipe.ingredients.map((ing, i) => (
                <li key={i}>
                  {ing.name}
                  {ing.quantity ? ` ${ing.quantity}` : ""}
                  {ing.unit ? ing.unit : ""}
                </li>
              ))}
            </ul>

            {recipe.instructions && (
              <>
                <h2>作り方</h2>
                <div className="recipe-detail__instructions">
                  <ol>
                    {recipe.instructions
                      .split(/\n+/)
                      .filter((s) => s.trim())
                      .map((step, i) => (
                        <li key={i}>{step}</li>
                      ))}
                  </ol>
                </div>
              </>
            )}
          </article>
        )}
      </div>
    </main>
  );
}
