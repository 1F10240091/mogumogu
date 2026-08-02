'use client';

import { Recipe } from '@/lib/api';
import Link from 'next/link';

interface RecipeCardProps {
  recipe: Recipe;
}

const categoryLabels: Record<string, string> = {
  main_dish: '主菜',
  side_dish: '副菜',
  soup: '汁物',
  rice: 'ごはん',
  noodle: '麺類',
  dessert: 'デザート',
  other: 'その他',
};

export function RecipeCard({ recipe }: RecipeCardProps) {
  const formatTime = (minutes: number | null) => {
    if (!minutes) return '不明';
    if (minutes < 60) return `${minutes}分`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return mins > 0 ? `${hours}時間${mins}分` : `${hours}時間`;
  };

  return (
    <Link
      href={`/recipes/${recipe.id}`}
      className="group block bg-white rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow overflow-hidden h-full flex flex-col"
    >
      {recipe.image_url ? (
        <div className="aspect-video relative overflow-hidden bg-gray-100">
          <img
            src={recipe.image_url}
            alt={recipe.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            loading="lazy"
          />
        </div>
      ) : (
        <div className="aspect-video relative overflow-hidden bg-gray-100 flex items-center justify-center">
          <svg
            className="w-16 h-16 text-gray-300"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
        </div>
      )}
      <div className="p-4 flex flex-col flex-1">
        <div className="flex items-center gap-2 mb-2">
          <span className="px-2 py-1 text-xs font-medium bg-orange-100 text-orange-700 rounded-full">
            {categoryLabels[recipe.category] || recipe.category}
          </span>
          {recipe.cooking_time_minutes && (
            <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-700 rounded-full">
              {formatTime(recipe.cooking_time_minutes)}
            </span>
          )}
        </div>
        <h3 className="font-semibold text-gray-900 text-lg mb-1 line-clamp-2 group-hover:text-orange-600 transition-colors">
          {recipe.title}
        </h3>
        {recipe.description && (
          <p className="text-gray-600 text-sm mb-3 line-clamp-2 flex-1">{recipe.description}</p>
        )}
        <div className="flex flex-wrap gap-1 mt-auto">
          {recipe.ingredients.slice(0, 3).map((ingredient, index) => (
            <span
              key={index}
              className="px-2 py-0.5 text-xs bg-gray-50 text-gray-600 rounded border"
            >
              {ingredient}
            </span>
          ))}
          {recipe.ingredients.length > 3 && (
            <span className="px-2 py-0.5 text-xs bg-gray-50 text-gray-500 rounded border">
              +{recipe.ingredients.length - 3}個
            </span>
          )}
        </div>
      </div>
    </Link>
  );
}
