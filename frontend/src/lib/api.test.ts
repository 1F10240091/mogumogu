import { ApiClient } from '@/lib/api';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const mockRecipe = {
  id: '11111111-1111-1111-1111-111111111111',
  title: 'にんじんのやわらか煮',
  description: '離乳食後期から食べられる、やわらかく煮たにんじん。',
  category: 'side_dish',
  ingredients: ['にんじん 1本', 'だし汁 適量'],
  instructions: ['にんじんをやわらかくゆでる', '細かく刻んでだし汁で煮る'],
  cooking_time_minutes: 15,
  servings: 2,
  image_url: null,
  source_url: null,
  tags: ['離乳食', '後期'],
  created_at: '2026-08-01T00:00:00Z',
  is_public: true,
};

describe('ApiClient', () => {
  let client: ApiClient;

  beforeEach(() => {
    client = new ApiClient('http://test-api.example.com');
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('should search recipes and build query params', async () => {
    const mockResponse = {
      recipes: [mockRecipe],
      total: 1,
      page: 1,
      per_page: 20,
      total_pages: 1,
    };
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => mockResponse,
    } as Response);

    const result = await client.searchRecipes({
      keyword: 'にんじん',
      category: 'side_dish',
      ingredients: ['にんじん'],
      max_cooking_time: 30,
      page: 2,
    });

    expect(fetch).toHaveBeenCalledTimes(1);
    const [url, init] = vi.mocked(fetch).mock.calls[0];
    expect(String(url)).toContain('/recipes?');
    expect(String(url)).toContain('keyword=' + encodeURIComponent('にんじん'));
    expect(String(url)).toContain('category=side_dish');
    expect(String(url)).toContain('ingredients=' + encodeURIComponent('にんじん'));
    expect(String(url)).toContain('max_cooking_time=30');
    expect(String(url)).toContain('page=2');
    expect(init?.headers).toMatchObject({ 'Content-Type': 'application/json' });

    expect(result).toEqual(mockResponse);
  });

  it('should get a single recipe by id', async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => mockRecipe,
    } as Response);

    const result = await client.getRecipe(mockRecipe.id);
    expect(fetch).toHaveBeenCalledWith(
      `http://test-api.example.com/recipes/${mockRecipe.id}`,
      expect.objectContaining({ headers: { 'Content-Type': 'application/json' } })
    );
    expect(result).toEqual(mockRecipe);
  });

  it('should throw an error when the response is not ok', async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: false,
      status: 404,
      json: async () => ({ detail: 'Recipe not found' }),
    } as Response);

    await expect(client.getRecipe(mockRecipe.id)).rejects.toThrow('Recipe not found');
  });

  it('should omit undefined query params', async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ recipes: [], total: 0, page: 1, per_page: 20, total_pages: 0 }),
    } as Response);

    await client.searchRecipes({});

    const url = String(vi.mocked(fetch).mock.calls[0][0]);
    expect(url).toBe('http://test-api.example.com/recipes?');
  });

  it('should encode ingredients array as repeated params', async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => ({ recipes: [], total: 0, page: 1, per_page: 20, total_pages: 0 }),
    } as Response);

    await client.searchRecipes({ ingredients: ['にんじん', 'たまねぎ'] });

    const url = String(vi.mocked(fetch).mock.calls[0][0]);
    expect(url).toContain('ingredients=' + encodeURIComponent('にんじん'));
    expect(url).toContain('ingredients=' + encodeURIComponent('たまねぎ'));
  });
});
