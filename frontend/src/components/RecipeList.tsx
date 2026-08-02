'use client';

import { RecipeSearchResponse } from '@/lib/api';
import { RecipeCard } from './RecipeCard';

interface RecipeListProps {
  data: RecipeSearchResponse;
  onPageChange: (page: number) => void;
}

export function RecipeList({ data, onPageChange }: RecipeListProps) {
  const { recipes, total, page, per_page, total_pages } = data;

  if (recipes.length === 0) {
    return (
      <div className="text-center py-12">
        <svg
          className="mx-auto h-16 w-16 text-gray-300"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1}
            d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <h3 className="mt-2 text-lg font-medium text-gray-900">レシピが見つかりません</h3>
        <p className="mt-1 text-gray-500">検索条件を変更して再度お試しください</p>
      </div>
    );
  }

  const getPageNumbers = () => {
    const pages: (number | string)[] = [];
    const maxVisible = 5;
    let start = Math.max(1, page - Math.floor(maxVisible / 2));
    let end = Math.min(total_pages, start + maxVisible - 1);

    if (end - start + 1 < maxVisible) {
      start = Math.max(1, end - maxVisible + 1);
    }

    if (start > 1) {
      pages.push(1);
      if (start > 2) pages.push('...');
    }

    for (let i = start; i <= end; i++) {
      pages.push(i);
    }

    if (end < total_pages) {
      if (end < total_pages - 1) pages.push('...');
      pages.push(total_pages);
    }

    return pages;
  };

  const pageNumbers = getPageNumbers();

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {recipes.map((recipe) => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </div>

      {total_pages > 1 && (
        <nav className="mt-8 flex items-center justify-center gap-1" aria-label="Pagination">
          <button
            onClick={() => onPageChange(page - 1)}
            disabled={page === 1}
            className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-l-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            aria-label="前のページ"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 19l-7-7 7-7"
              />
            </svg>
          </button>

          {pageNumbers.map((pageNum, index) =>
            pageNum === '...' ? (
              <span key={`ellipsis-${index}`} className="px-3 py-2 text-sm text-gray-500">
                ...
              </span>
            ) : (
              <button
                key={pageNum}
                onClick={() => onPageChange(pageNum as number)}
                className={`px-4 py-2 text-sm font-medium border ${
                  pageNum === page
                    ? 'bg-orange-600 text-white border-orange-600'
                    : 'text-gray-500 bg-white border-gray-300 hover:bg-gray-50'
                } ${index === 0 ? 'rounded-l-lg' : index === pageNumbers.length - 1 ? 'rounded-r-lg' : ''}`}
                aria-label={`ページ ${pageNum}`}
                aria-current={pageNum === page ? 'page' : undefined}
              >
                {pageNum}
              </button>
            )
          )}

          <button
            onClick={() => onPageChange(page + 1)}
            disabled={page === total_pages}
            className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-r-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
            aria-label="次のページ"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </nav>
      )}

      <div className="mt-4 text-center text-sm text-gray-500">
        {total > 0 ? (
          <>
            {(page - 1) * per_page + 1}〜{Math.min(page * per_page, total)} 件 / 全 {total} 件
          </>
        ) : (
          'レシピがありません'
        )}
      </div>
    </>
  );
}
