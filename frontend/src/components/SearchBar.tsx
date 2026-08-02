'use client';

import { ChangeEvent, FormEvent, useState } from 'react';

interface SearchBarProps {
  onSearch: (params: {
    keyword?: string;
    category?: string;
    ingredients?: string[];
    maxCookingTime?: number;
  }) => void;
  initialKeyword?: string;
  initialCategory?: string;
}

export function SearchBar({ onSearch, initialKeyword = '', initialCategory = '' }: SearchBarProps) {
  const [keyword, setKeyword] = useState(initialKeyword);
  const [category, setCategory] = useState(initialCategory);
  const [ingredients, setIngredients] = useState('');
  const [maxCookingTime, setMaxCookingTime] = useState('');

  const categories = [
    { value: '', label: 'すべて' },
    { value: 'main_dish', label: '主菜' },
    { value: 'side_dish', label: '副菜' },
    { value: 'soup', label: '汁物' },
    { value: 'rice', label: 'ごはん' },
    { value: 'noodle', label: '麺類' },
    { value: 'dessert', label: 'デザート' },
    { value: 'other', label: 'その他' },
  ];

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSearch({
      keyword: keyword || undefined,
      category: category || undefined,
      ingredients: ingredients ? ingredients.split(',').map((s) => s.trim()) : undefined,
      maxCookingTime: maxCookingTime ? parseInt(maxCookingTime) : undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 bg-white rounded-lg shadow-sm border">
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <label htmlFor="keyword" className="block text-sm font-medium text-gray-700 mb-1">
            キーワード
          </label>
          <input
            type="text"
            id="keyword"
            value={keyword}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setKeyword(e.target.value)}
            placeholder="レシピ名、材料などで検索"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          />
        </div>
        <div className="w-full sm:w-48">
          <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
            カテゴリ
          </label>
          <select
            id="category"
            value={category}
            onChange={(e: ChangeEvent<HTMLSelectElement>) => setCategory(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          >
            {categories.map((cat) => (
              <option key={cat.value} value={cat.value}>
                {cat.label}
              </option>
            ))}
          </select>
        </div>
      </div>
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <label htmlFor="ingredients" className="block text-sm font-medium text-gray-700 mb-1">
            材料（カンマ区切り）
          </label>
          <input
            type="text"
            id="ingredients"
            value={ingredients}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setIngredients(e.target.value)}
            placeholder="例: にんじん, 玉ねぎ, 豚肉"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          />
        </div>
        <div className="w-full sm:w-48">
          <label htmlFor="maxCookingTime" className="block text-sm font-medium text-gray-700 mb-1">
            調理時間（分以内）
          </label>
          <input
            type="number"
            id="maxCookingTime"
            value={maxCookingTime}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setMaxCookingTime(e.target.value)}
            placeholder="例: 30"
            min="1"
            max="180"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          />
        </div>
      </div>
      <div className="flex justify-end pt-2">
        <button
          type="submit"
          className="px-6 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 transition-colors"
        >
          検索
        </button>
      </div>
    </form>
  );
}
