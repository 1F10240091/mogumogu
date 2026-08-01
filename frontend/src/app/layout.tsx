import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "ほいく献立",
  description: "保育園の献立を活かした家庭の夕食提案サービス",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
