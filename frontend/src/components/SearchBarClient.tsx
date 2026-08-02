'use client';

import { SearchBar } from '@/components/SearchBar';
import { useRouter, useSearchParams } from 'next/navigation';

interface SearchBarClientProps {
  initialKeyword: string;
  initialCategory: string;
}

export function SearchBarClient({ initialKeyword, initialCategory }: SearchBarClientProps) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const handleSearch = (params: {
    keyword?: string;
    category?: string;
    ingredients?: string[];
    maxCookingTime?: number;
  }) => {
    const next = new URLSearchParams(searchParams.toString());

    if (params.keyword) next.set('keyword', params.keyword);
    else next.delete('keyword');

    if (params.category) next.set('category', params.category);
    else next.delete('category');

    next.delete('ingredients');
    params.ingredients?.forEach((i) => next.append('ingredients', i));

    if (params.maxCookingTime) next.set('max_cooking_time', String(params.maxCookingTime));
    else next.delete('max_cooking_time');

    next.set('page', '1');

    router.push(`/recipes?${next.toString()}`);
  };

  return (
    <SearchBar
      onSearch={handleSearch}
      initialKeyword={initialKeyword}
      initialCategory={initialCategory}
    />
  );
}
