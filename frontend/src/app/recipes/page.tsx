import { RecipeListClient } from '@/components/RecipeListClient';
import { SearchBarClient } from '@/components/SearchBarClient';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'レシピ検索 | もぐもぐ',
  description: '離乳食・幼児食レシピを検索。材料、カテゴリ、調理時間で絞り込み可能。',
};

interface RecipesPageProps {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}

function toArray(value: string | string[] | undefined): string[] {
  if (!value) return [];
  return Array.isArray(value) ? value : [value];
}

export default async function RecipesPage({ searchParams }: RecipesPageProps) {
  const params = await searchParams;

  const keyword = toArray(params.keyword)[0];
  const category = toArray(params.category)[0];
  const page = parseInt(toArray(params.page)[0] || '1', 10) || 1;
  const perPage = parseInt(toArray(params.per_page)[0] || '20', 10) || 20;
  const maxCookingTime = parseInt(toArray(params.max_cooking_time)[0] || '', 10);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const query = new URLSearchParams();
  if (keyword) query.append('keyword', keyword);
  if (category) query.append('category', category);
  toArray(params.ingredients).forEach((i) => query.append('ingredients', i));
  toArray(params.tags).forEach((t) => query.append('tags', t));
  if (maxCookingTime) query.append('max_cooking_time', String(maxCookingTime));
  query.append('page', String(page));
  query.append('per_page', String(perPage));

  const response = await fetch(`${apiUrl}/recipes?${query.toString()}`, {
    next: { revalidate: 60 },
  });

  const data = response.ok
    ? await response.json()
    : { recipes: [], total: 0, page: 1, per_page: 20, total_pages: 0 };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <h1 className="text-2xl font-bold text-gray-900">レシピ検索</h1>
            <nav className="flex items-center gap-4">
              <a href="/" className="text-gray-600 hover:text-gray-900">
                ホーム
              </a>
              <a href="/recipes" className="text-orange-600 font-medium">
                レシピ
              </a>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="lg:grid lg:grid-cols-4 lg:gap-8">
          <aside className="lg:col-span-1">
            <SearchBarClient initialKeyword={keyword || ''} initialCategory={category || ''} />
          </aside>
          <div className="lg:col-span-3 mt-6 lg:mt-0">
            <RecipeListClient
              initialData={data}
              keyword={keyword}
              category={category}
              ingredients={toArray(params.ingredients)}
              tags={toArray(params.tags)}
              maxCookingTime={maxCookingTime}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
