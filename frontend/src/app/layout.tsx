import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MoguMogu | 保育園児の親向け献立自動生成",
  description:
    "保育園の献立表を読み取り、アレルギー・好き嫌い・冷蔵庫の在庫を考慮した夕食献立を AI が自動提案します。",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#f59e0b",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
