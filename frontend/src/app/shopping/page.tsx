"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import AppNav from "@/components/AppNav";
import RequireAuth from "@/components/RequireAuth";
import { api, type ShoppingItem } from "@/lib/api";

export default function ShoppingPage() {
  const [items, setItems] = useState<ShoppingItem[]>([]);
  const [inventory, setInventory] = useState<ShoppingItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [newItem, setNewItem] = useState("");
  const [error, setError] = useState<string | null>(null);

  const load = () => {
    setLoading(true);
    Promise.all([api.getShoppingList(), api.listInventory()])
      .then(([list, inv]) => {
        setItems(list.items);
        setInventory(inv);
      })
      .catch((err) =>
        setError(err instanceof Error ? err.message : "読み込みに失敗しました"),
      )
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleAdd = async () => {
    const name = newItem.trim();
    if (!name) return;
    setError(null);
    try {
      await api.addInventory(name);
      setNewItem("");
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "追加に失敗しました");
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await api.deleteInventory(id);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "削除に失敗しました");
    }
  };

  return (
    <RequireAuth>
      <main className="main">
      <AppNav />
      <div className="container" style={{ paddingBottom: 80 }}>
        <div className="page-header">
          <h1 className="page-header__title">買い物リスト</h1>
          <p className="page-header__subtitle">
            献立で不足している食材と、冷蔵庫の在庫を確認できます。
          </p>
        </div>
        {error && <div className="alert alert--error">{error}</div>}
        {loading ? (
          <div className="loading">読み込み中...</div>
        ) : items.length === 0 ? (
          <div className="card">
            <p className="card__text">
              まだ不足食材がありません。先に AI
              献立提案で献立を生成してください。
            </p>
            <Link href="/meal-plan" className="button">
              献立を作成する
            </Link>
          </div>
        ) : (
          <div className="card">
            <h2 className="card__title">不足食材</h2>
            <ul className="list">
              {items.map((item) => (
                <li key={item.name} className="list__item">
                  <div>
                    <p className="list__item-title">{item.name}</p>
                    {item.needed && (
                      <p className="list__item-text">
                        必要合計分量: {item.needed}
                      </p>
                    )}
                    {item.source_recipes && item.source_recipes.length > 0 && (
                      <p className="list__item-text">
                        必要レシピ: {item.source_recipes.join("、")}
                      </p>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        <h2 className="section-heading" style={{ marginTop: 40, border: "none" }}>
          冷蔵庫の在庫
        </h2>
        <div className="card">
          <div className="input-row" style={{ marginBottom: 8 }}>
            <input
              value={newItem}
              onChange={(e) => setNewItem(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleAdd()}
              placeholder="食材名（例: 玉ねぎ）"
              className="input"
            />
            <button
              className="button"
              onClick={handleAdd}
              disabled={!newItem.trim()}
            >
              追加
            </button>
          </div>
          {inventory.length === 0 ? (
            <p className="card__text">在庫はまだありません。</p>
          ) : (
            <ul className="list">
              {inventory.map((item) => (
                <li key={item.id ?? item.name} className="list__item">
                  <span>{item.name}</span>
                  <button
                    onClick={() => handleDelete(item.id!)}
                    className="button button--danger button--sm"
                  >
                    削除
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
      </main>
    </RequireAuth>
  );
}
