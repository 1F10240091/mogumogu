const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Recipe {
  id: string;
  title: string;
  description: string | null;
  category: string;
  ingredients: string[];
  instructions: string[];
  cooking_time_minutes: number | null;
  servings: number | null;
  image_url: string | null;
  source_url: string | null;
  tags: string[];
  created_at: string;
  is_public: boolean;
}

export const RecipeCategory = {
  MAIN_DISH: 'main_dish',
  SIDE_DISH: 'side_dish',
  SOUP: 'soup',
  RICE: 'rice',
  NOODLE: 'noodle',
  DESSERT: 'dessert',
  OTHER: 'other',
} as const;

export type RecipeCategoryValue = (typeof RecipeCategory)[keyof typeof RecipeCategory];

export interface RecipeSearchResponse {
  recipes: Recipe[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export interface RecipeSearchParams {
  keyword?: string;
  category?: string;
  ingredients?: string[];
  tags?: string[];
  max_cooking_time?: number;
  page?: number;
  per_page?: number;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  getBaseUrl(): string {
    return this.baseUrl;
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async searchRecipes(params: RecipeSearchParams = {}): Promise<RecipeSearchResponse> {
    const searchParams = new URLSearchParams();

    if (params.keyword) searchParams.append('keyword', params.keyword);
    if (params.category) searchParams.append('category', params.category);
    if (params.ingredients)
      params.ingredients.forEach((i) => searchParams.append('ingredients', i));
    if (params.tags) params.tags.forEach((t) => searchParams.append('tags', t));
    if (params.max_cooking_time)
      searchParams.append('max_cooking_time', params.max_cooking_time.toString());
    if (params.page) searchParams.append('page', params.page.toString());
    if (params.per_page) searchParams.append('per_page', params.per_page.toString());

    return this.request<RecipeSearchResponse>(`/recipes?${searchParams.toString()}`);
  }

  async getRecipe(id: string): Promise<Recipe> {
    return this.request<Recipe>(`/recipes/${id}`);
  }
}

export { ApiClient };
export const apiClient = new ApiClient();
