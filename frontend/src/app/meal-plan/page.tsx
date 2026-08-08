"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import AppNav from "@/components/AppNav";
import RequireAuth from "@/components/RequireAuth";
import { api, type Child, type GenerateResponse, type SuggestedMeal } from "@/lib/api";

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
        const inner = (
          <span className="meal-dish__label">{dish}</span>
        );
        return (
          <li key={`${dish}-${i}`} className="meal-dish">
            {recipeId ? (
              <Link href={`/recipe-master/${recipeId}`}>{inner}</Link>
            ) : (
              <Link href={`/recipe-search?keyword=${encodeURIComponent(dish)}`}>
                {inner}
              </Link>
            )}
          </li>
        );
      })}
    </ul>
  );
}

export default function MealPlanPage() {
  const [children, setChildren] = useState<Child[]>([]);
  const [selectedChild, setSelectedChild] = useState("");
  const [date, setDate] = useState(() => {
    const now = new Date();
    const pad = (n: number) => String(n).padStart(2, "0");
    return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
  });
  const [days, setDays] = useState(7);
  const [mealPlan, setMealPlan] = useState<GenerateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.listChildren().then((list) => {
      setChildren(list);
      if (list.length > 0) setSelectedChild(list[0].id);
    }).catch((err) =>
      setError(err instanceof Error ? err.message : "子どもの読み込みに失敗しました"),
    );
  }, []);

  const handleGenerate = async () => {
    setError(null);
    try {
      const result = await api.generateRecipe(selectedChild, date, days);
      setMealPlan(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "献立の生成に失敗しました");
    }
  };

  return (
    <RequireAuth>
      <main className="main">
      <AppNav />
      <div className="container" style={{ paddingBottom: 80 }}>
        <div className="page-header">
          <h1 className="page-header__title">AI 献立提案</h1>
          <p className="page-header__subtitle">
            お子様の情報と在庫を考慮した夕食献立を AI が自動提案します。
          </p>
        </div>
        <div className="card">
          <label className="form-field">
            <span className="form-field__label">お子様</span>
            <select
              value={selectedChild}
              onChange={(e) => setSelectedChild(e.target.value)}
              className="select"
            >
              {children.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </label>
          <label className="form-field">
            <span className="form-field__label">開始日</span>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="input"
            />
          </label>
          <label className="form-field">
            <span className="form-field__label">日数</span>
            <select
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="select"
            >
              {[1, 2, 3, 4, 5, 6, 7].map((n) => (
                <option key={n} value={n}>
                  {n} 日分
                </option>
              ))}
            </select>
          </label>
          {error && <div className="alert alert--error">{error}</div>}
          <button
            className="button"
            onClick={handleGenerate}
            disabled={!selectedChild}
          >
            献立を生成する
          </button>
        </div>

        {mealPlan && mealPlan.meals.length > 0 && (
          <div style={{ marginTop: 24 }}>
            <h2 className="page-header__title">
              提案された献立（{mealPlan.meals.length} 日分）
            </h2>
            {mealPlan.meals.map((meal) => (
              <div className="card" key={meal.id}>
                <h3>{meal.date}</h3>
                <MealDishes meal={meal} />
              </div>
            ))}
            <div className="action-links">
              <Link href="/recipes" className="button">
                レシピ・買い物リストを見る
              </Link>
            </div>
          </div>
        )}
      </div>
      </main>
    </RequireAuth>
  );
}
