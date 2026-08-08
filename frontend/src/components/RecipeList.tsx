"use client";

import { useRouter, useSearchParams } from "next/navigation";
import RecipeCard from "./RecipeCard";
import type { RecipeSearchResponse } from "@/lib/api";

interface RecipeListProps {
  result: RecipeSearchResponse;
}

export default function RecipeList({ result }: RecipeListProps) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const goToPage = (page: number) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set("page", String(page));
    router.push(`/recipe-search?${params.toString()}`);
  };

  if (result.total === 0) {
    return (
      <div className="card">
        <p>条件に一致するレシピが見つかりませんでした。</p>
      </div>
    );
  }

  return (
    <>
      <p style={{ color: "var(--color-muted)", fontSize: 14 }}>
        {result.total}件のレシピが見つかりました
      </p>
      <div className="recipe-grid">
        {result.recipes.map((recipe) => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>
      {result.total_pages > 1 && (
        <nav className="pagination" aria-label="ページ送り">
          <button
            disabled={result.page <= 1}
            onClick={() => goToPage(result.page - 1)}
          >
            前へ
          </button>
          <span>
            {result.page} / {result.total_pages}
          </span>
          <button
            disabled={result.page >= result.total_pages}
            onClick={() => goToPage(result.page + 1)}
          >
            次へ
          </button>
        </nav>
      )}
    </>
  );
}
