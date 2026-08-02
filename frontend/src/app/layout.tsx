import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'もぐもぐ - 離乳食・幼児食レシピ検索',
  description:
    '保育園の献立を活かした家庭の夕食を自動提案します。離乳食・幼児食のレシピを検索できます。',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
