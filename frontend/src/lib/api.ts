// バックエンド API クライアント
const API_BASE = "/api/v1";

// FastAPI のエラーレスポンスを日本語のわかりやすいメッセージに変換する
function friendlyError(body: string, status: number): string {
  if (status === 401) return "メールアドレスまたはパスワードが正しくありません";
  if (status === 403) return "この操作を行う権限がありません";
  if (status === 404) return "対象が見つかりませんでした";
  if (status === 409) return "既に登録されています";
  if (status === 500) return "サーバーでエラーが発生しました。時間をおいて再度お試しください";

  try {
    const parsed = JSON.parse(body);
    const detail = parsed?.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail.length > 0) {
      const first = detail[0];
      if (first?.loc?.includes("email")) return "メールアドレスの形式が正しくありません";
      if (first?.loc?.includes("password")) return "パスワードを確認してください";
      return "入力内容に誤りがあります";
    }
    if (typeof detail === "object" && detail !== null) {
      return "入力内容に誤りがあります";
    }
  } catch {
    // JSON でない場合はそのまま本文を返す
  }
  return body || "通信に失敗しました";
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  };

  const isFormData = options.body instanceof FormData;
  if (!isFormData && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  const token = localStorage.getItem("token");
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(friendlyError(body, res.status));
  }
  return res.json() as Promise<T>;
}

export interface User {
  id: string;
  email: string;
  display_name: string | null;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface Child {
  id: string;
  name: string;
  birth_date: string | null;
  allergies: { id: string; ingredient: string }[];
  preferences: { id: string; ingredient: string; mode: string }[];
}

export interface NurseryMenu {
  id: string;
  date: string;
  menu_text: string;
  ingredients: Record<string, unknown>;
}

export interface SuggestedMeal {
  id: string;
  date: string;
  menu_text: string;
  ingredients: Record<string, unknown>;
}

export interface GenerateResponse {
  meals: SuggestedMeal[];
}

export interface ShoppingItem {
  id?: string;
  name: string;
  quantity?: string | null;
  unit?: string;
  needed?: string;
  source_recipes?: string[];
}

export interface ShoppingList {
  items: ShoppingItem[];
  generated_at: string;
}

export interface Recipe {
  id: string;
  name: string;
  meal_type: string;
  ingredients: { name: string; quantity?: string; unit?: string }[];
  instructions: string;
  cook_time_minutes?: number | null;
}

export interface RecipeSearchParams {
  keyword?: string;
  meal_type?: string;
  ingredient?: string;
  max_cook_time?: number;
  page?: number;
  per_page?: number;
}

export interface RecipeSearchResponse {
  recipes: Recipe[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

const realApi = {
  register(email: string, password: string, displayName?: string) {
    return request<TokenResponse>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, display_name: displayName }),
    });
  },
  login(email: string, password: string) {
    return request<TokenResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  },
  me() {
    return request<User>("/auth/me");
  },
  updateMe(payload: { display_name?: string; password?: string }) {
    return request<User>("/auth/me", {
      method: "PUT",
      body: JSON.stringify(payload),
    });
  },
  listChildren() {
    return request<Child[]>("/children");
  },
  createChild(payload: Omit<Child, "id">) {
    return request<Child>("/children", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
  updateChild(
    childId: string,
    payload: { name?: string; birth_date?: string | null },
  ) {
    return request<Child>(`/children/${childId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
  },
  deleteChild(childId: string) {
    return request<void>(`/children/${childId}`, { method: "DELETE" });
  },
  addAllergy(childId: string, ingredient: string) {
    return request<Child>(`/children/${childId}/allergies`, {
      method: "POST",
      body: JSON.stringify({ ingredient }),
    });
  },
  deleteAllergy(childId: string, allergyId: string) {
    return request<Child>(`/children/${childId}/allergies/${allergyId}`, {
      method: "DELETE",
    });
  },
  addPreference(childId: string, ingredient: string, mode: string) {
    return request<Child>(`/children/${childId}/preferences`, {
      method: "POST",
      body: JSON.stringify({ ingredient, mode }),
    });
  },
  deletePreference(childId: string, preferenceId: string) {
    return request<Child>(`/children/${childId}/preferences/${preferenceId}`, {
      method: "DELETE",
    });
  },
  listMenus() {
    return request<NurseryMenu[]>("/menus");
  },
  uploadMenu(file: File) {
    const formData = new FormData();
    formData.append("file", file);
    return request<NurseryMenu>("/menus/upload", {
      method: "POST",
      body: formData,
    });
  },
  listRecipes() {
    return request<Recipe[]>("/recipe-master");
  },
  searchRecipes(params: RecipeSearchParams = {}) {
    const sp = new URLSearchParams();
    if (params.keyword) sp.set("keyword", params.keyword);
    if (params.meal_type) sp.set("meal_type", params.meal_type);
    if (params.ingredient) sp.set("ingredient", params.ingredient);
    if (params.max_cook_time)
      sp.set("max_cook_time", String(params.max_cook_time));
    if (params.page) sp.set("page", String(params.page));
    if (params.per_page) sp.set("per_page", String(params.per_page));
    const qs = sp.toString();
    return request<RecipeSearchResponse>(
      `/recipe-master/search${qs ? `?${qs}` : ""}`,
    );
  },
  getRecipe(recipeId: string) {
    return request<Recipe>(`/recipe-master/${recipeId}`);
  },
  listMealRecipes() {
    return request<SuggestedMeal[]>("/recipes");
  },
  generateRecipe(childId: string, menuDate: string, days = 7) {
    return request<GenerateResponse>("/recipes/generate", {
      method: "POST",
      body: JSON.stringify({ child_id: childId, menu_date: menuDate, days }),
    });
  },
  getShoppingList() {
    return request<ShoppingList>("/shopping/list");
  },
  listInventory() {
    return request<ShoppingItem[]>("/shopping/inventory");
  },
  addInventory(name: string, quantity?: string) {
    return request<ShoppingItem>("/shopping/inventory", {
      method: "POST",
      body: JSON.stringify({ name, quantity }),
    });
  },
  deleteInventory(id: string) {
    return request<void>(`/shopping/inventory/${id}`, { method: "DELETE" });
  },
  submitFeedback(rating: number | null, comment: string) {
    return request<{ id: string; rating: number | null; comment: string }>(
      "/feedback",
      {
        method: "POST",
        body: JSON.stringify({ rating, comment }),
      },
    );
  },
};

// 常時バックエンド API を利用する（デモモードは廃止）
export const api = realApi;
