"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_ITEMS = [
  { href: "/dashboard", label: "ホーム" },
  { href: "/menus", label: "献立表" },
  { href: "/meal-plan", label: "AI 献立提案" },
  { href: "/recipe-search", label: "レシピ検索" },
  { href: "/recipes", label: "提案献立" },
  { href: "/shopping", label: "買い物リスト" },
  { href: "/feedback", label: "フィードバック" },
];

export default function AppNav() {
  const pathname = usePathname();

  return (
    <>
      <a href="#main-content" className="skip-link">
        メインコンテンツへスキップ
      </a>
      <nav className="app-nav" aria-label="メインナビゲーション">
        <div className="app-nav__inner">
          <Link href="/dashboard" className="app-nav__brand">
            もぐもぐ
          </Link>
          <ul className="app-nav__list">
            {NAV_ITEMS.map((item) => {
              const active = pathname.startsWith(item.href);
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={`app-nav__link${active ? " app-nav__link--active" : ""}`}
                  >
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      </nav>
    </>
  );
}
