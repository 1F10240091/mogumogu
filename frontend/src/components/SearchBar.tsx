"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const MEAL_TYPE_LABELS: Record<string, string> = {
  main: "主菜",
  side: "副菜",
  soup: "汁物",
  staple: "主食",
};

interface SearchBarProps {
  initial?: {
    keyword?: string;
    meal_type?: string;
    ingredient?: string;
    max_cook_time?: number;
  };
}

export default function SearchBar({ initial = {} }: SearchBarProps) {
  const router = useRouter();
  const [keyword, setKeyword] = useState(initial.keyword ?? "");
  const [mealType, setMealType] = useState(initial.meal_type ?? "");
  const [ingredient, setIngredient] = useState(initial.ingredient ?? "");
  const [maxCookTime, setMaxCookTime] = useState(
    initial.max_cook_time ? String(initial.max_cook_time) : "",
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (keyword.trim()) params.set("keyword", keyword.trim());
    if (mealType) params.set("meal_type", mealType);
    if (ingredient.trim()) params.set("ingredient", ingredient.trim());
    if (maxCookTime) params.set("max_cook_time", maxCookTime);
    router.push(`/recipe-search?${params.toString()}`);
  };

  return (
    <form
      className="card search-form"
      onSubmit={handleSubmit}
      aria-label="レシピ検索"
    >
      <div className="search-form__field">
        <label htmlFor="search-keyword">キーワード</label>
        <input
          id="search-keyword"
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="レシピ名や作り方で検索"
        />
      </div>
      <div className="search-form__field">
        <label htmlFor="search-meal-type">カテゴリ</label>
        <select
          id="search-meal-type"
          value={mealType}
          onChange={(e) => setMealType(e.target.value)}
        >
          <option value="">すべて</option>
          {Object.entries(MEAL_TYPE_LABELS).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </div>
      <div className="search-form__field">
        <label htmlFor="search-ingredient">材料</label>
        <input
          id="search-ingredient"
          type="text"
          value={ingredient}
          onChange={(e) => setIngredient(e.target.value)}
          placeholder="例: にんじん, 豚肉"
        />
      </div>
      <div className="search-form__field">
        <label htmlFor="search-max-time">調理時間（分以内）</label>
        <input
          id="search-max-time"
          type="number"
          min={1}
          max={180}
          value={maxCookTime}
          onChange={(e) => setMaxCookTime(e.target.value)}
          placeholder="例: 30"
        />
      </div>
      <div className="search-form__actions">
        <button type="submit" className="button">
          検索
        </button>
      </div>
    </form>
  );
}
