"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import AppNav from "@/components/AppNav";
import RequireAuth from "@/components/RequireAuth";
import { api, type SuggestedMeal } from "@/lib/api";

function MealDishes({ meal }: { meal: SuggestedMeal }) {
  const ingredients = (meal.ingredients ?? {}) as {
    dishes?: string[];
    recipe_ids?: string[];
  };
  const dishes = ingredients.dishes ?? [];
  const recipeIds = ingredients.recipe_ids ?? [];

  if (dishes.length === 0) {
    return (
      <pre
        style={{ whiteSpace: "pre-wrap", fontFamily: "inherit", margin: 0 }}
      >
        {meal.menu_text}
      </pre>
    );
  }

  return (
    <ul className="meal-dishes" style={{ listStyle: "none", margin: 0 }}>
      {dishes.map((dish, i) => {
        const recipeId = recipeIds[i];
        return (
          <li key={`${dish}-${i}`} className="meal-dish">
            {recipeId ? (
              <Link href={`/recipe-master/${recipeId}`}>
                <span className="meal-dish__label">{dish}</span>
              </Link>
            ) : (
              <Link
                href={`/recipe-search?keyword=${encodeURIComponent(dish)}`}
              >
                <span className="meal-dish__label">{dish}</span>
              </Link>
            )}
          </li>
        );
      })}
    </ul>
  );
}

export default function RecipesPage() {
  const [recipes, setRecipes] = useState<SuggestedMeal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .listMealRecipes()
      .then(setRecipes)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "読み込みに失敗しました"),
      )
      .finally(() => setLoading(false));
  }, []);

  return (
    <RequireAuth>
      <main className="main">
      <AppNav />
      <div className="container" style={{ paddingBottom: 80 }}>
        <div className="page-header">
          <h1 className="page-header__title">レシピ・買い物リスト</h1>
          <p className="page-header__subtitle">
            AI が提案した献立の詳細を確認できます。料理名をクリックすると
            レシピの作り方が見られます。
          </p>
        </div>
        {error && <div className="alert alert--error">{error}</div>}
        {loading ? (
          <div className="loading">読み込み中...</div>
        ) : recipes.length === 0 ? (
          <div className="card">
            <p className="card__text">まだ提案された献立がありません。</p>
            <Link href="/meal-plan" className="button">
              献立を作成する
            </Link>
          </div>
        ) : (
          recipes.map((recipe) => (
            <div className="card" key={recipe.id}>
              <h2>{recipe.date}</h2>
              <MealDishes meal={recipe} />
</div>
            ))
          )}
      </div>
      </main>
      </RequireAuth>
  );
}
