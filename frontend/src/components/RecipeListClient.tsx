'use client';

import { RecipeList } from '@/components/RecipeList';
import { RecipeSearchResponse } from '@/lib/api';
import { useRouter, useSearchParams } from 'next/navigation';
import { useState } from 'react';

interface RecipeListClientProps {
  initialData: RecipeSearchResponse;
  keyword?: string;
  category?: string;
  ingredients?: string[];
  tags?: string[];
  maxCookingTime?: number;
}

export function RecipeListClient({
  initialData,
  keyword,
  category,
  ingredients = [],
  tags = [],
  maxCookingTime,
}: RecipeListClientProps) {
  const [data, setData] = useState<RecipeSearchResponse>(initialData);
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();

  const handlePageChange = async (page: number) => {
    setLoading(true);
    const next = new URLSearchParams(searchParams.toString());
    next.set('page', String(page));

    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/recipes?${next.toString()}`);

    if (response.ok) {
      setData(await response.json());
      router.push(`/recipes?${next.toString()}`, { scroll: false });
    }
    setLoading(false);
  };

  return (
    <div className="relative">
      <RecipeList data={data} onPageChange={handlePageChange} />
      {loading && (
        <div className="absolute inset-0 bg-white/50 flex items-center justify-center z-10">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-orange-600" />
        </div>
      )}
    </div>
  );
}
