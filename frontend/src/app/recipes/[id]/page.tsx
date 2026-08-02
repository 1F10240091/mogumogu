import { Recipe } from '@/lib/api';
import { Metadata } from 'next';
import { notFound } from 'next/navigation';

interface RecipeDetailPageProps {
  params: Promise<{ id: string }>;
}

export async function generateMetadata({ params }: RecipeDetailPageProps): Promise<Metadata> {
  const { id } = await params;
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  try {
    const response = await fetch(`${apiUrl}/recipes/${id}`, { next: { revalidate: 60 } });
    if (response.ok) {
      const recipe: Recipe = await response.json();
      return {
        title: `${recipe.title} | もぐもぐ`,
        description: recipe.description || `${recipe.title}のレシピ詳細`,
        openGraph: {
          title: recipe.title,
          description: recipe.description || '',
          images: recipe.image_url ? [recipe.image_url] : [],
          type: 'article',
        },
      };
    }
  } catch {
    // ignore
  }

  return { title: 'レシピ詳細 | もぐもぐ' };
}

export default async function RecipeDetailPage({ params }: RecipeDetailPageProps) {
  const { id } = await params;
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const response = await fetch(`${apiUrl}/recipes/${id}`, { next: { revalidate: 60 } });

  if (!response.ok) {
    notFound();
  }

  const recipe: Recipe = await response.json();

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <nav className="flex items-center gap-4">
              <a href="/" className="text-gray-600 hover:text-gray-900">
                ホーム
              </a>
              <a href="/recipes" className="text-gray-600 hover:text-gray-900">
                レシピ
              </a>
              <span className="text-gray-400">/</span>
              <span className="text-gray-900 font-medium truncate max-w-xs">{recipe.title}</span>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <article>
          <header className="mb-8">
            <span className="inline-block px-3 py-1 text-sm font-medium bg-orange-100 text-orange-700 rounded-full mb-4">
              {getCategoryLabel(recipe.category)}
            </span>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">{recipe.title}</h1>
            {recipe.description && <p className="text-lg text-gray-600">{recipe.description}</p>}
          </header>

          {recipe.image_url && (
            <div className="mb-8 rounded-lg overflow-hidden shadow-sm">
              <img src={recipe.image_url} alt={recipe.title} className="w-full h-auto" />
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
            <InfoCard
              title="調理時間"
              value={recipe.cooking_time_minutes ? `${recipe.cooking_time_minutes}分` : '不明'}
              icon={<ClockIcon />}
            />
            <InfoCard
              title="分量"
              value={recipe.servings ? `${recipe.servings}人分` : '不明'}
              icon={<UsersIcon />}
            />
            <InfoCard
              title="カテゴリ"
              value={getCategoryLabel(recipe.category)}
              icon={<TagIcon />}
            />
          </div>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <IngredientsIcon className="w-6 h-6 text-orange-600" />
              材料
            </h2>
            <ul className="space-y-2">
              {recipe.ingredients.map((ingredient, index) => (
                <li key={index} className="flex items-start gap-3 p-3 bg-white rounded-lg border">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-orange-100 text-orange-600 text-xs font-medium flex items-center justify-center">
                    {index + 1}
                  </span>
                  <span className="text-gray-700">{ingredient}</span>
                </li>
              ))}
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <InstructionsIcon className="w-6 h-6 text-orange-600" />
              作り方
            </h2>
            <ol className="space-y-4">
              {recipe.instructions.map((instruction, index) => (
                <li key={index} className="flex gap-4">
                  <span className="flex-shrink-0 w-8 h-8 rounded-full bg-orange-600 text-white text-sm font-medium flex items-center justify-center">
                    {index + 1}
                  </span>
                  <div className="pt-1">
                    <p className="text-gray-700 leading-relaxed">{instruction}</p>
                  </div>
                </li>
              ))}
            </ol>
          </section>

          {recipe.tags.length > 0 && (
            <section className="mb-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">タグ</h2>
              <div className="flex flex-wrap gap-2">
                {recipe.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </section>
          )}

          {recipe.source_url && (
            <section className="mb-8 p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">
                参照元:{' '}
                <a
                  href={recipe.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-orange-600 hover:underline"
                >
                  {recipe.source_url}
                </a>
              </p>
            </section>
          )}
        </article>
      </main>
    </div>
  );
}

function InfoCard({ title, value, icon }: { title: string; value: string; icon: React.ReactNode }) {
  return (
    <div className="bg-white p-4 rounded-lg border flex items-center gap-3">
      <div className="p-2 bg-orange-100 rounded-lg text-orange-600">{icon}</div>
      <div>
        <p className="text-xs text-gray-500">{title}</p>
        <p className="font-medium text-gray-900">{value}</p>
      </div>
    </div>
  );
}

function getCategoryLabel(category: string): string {
  const labels: Record<string, string> = {
    main_dish: '主菜',
    side_dish: '副菜',
    soup: '汁物',
    rice: 'ごはん',
    noodle: '麺類',
    dessert: 'デザート',
    other: 'その他',
  };
  return labels[category] || category;
}

function ClockIcon() {
  return (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
      />
    </svg>
  );
}

function UsersIcon() {
  return (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
      />
    </svg>
  );
}

function TagIcon() {
  return (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
      />
    </svg>
  );
}

function IngredientsIcon({ className = 'w-6 h-6' }: { className?: string }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M11 6l5.762 3.153a3.12 3.12 0 011.153 2.245V21a3.12 3.12 0 01-3.12 3.12H6a3.12 3.12 0 01-3.12-3.12V14.553a3.12 3.12 0 011.153-2.245L13 6z"
      />
    </svg>
  );
}

function InstructionsIcon({ className = 'w-6 h-6' }: { className?: string }) {
  return (
    <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
      />
    </svg>
  );
}
