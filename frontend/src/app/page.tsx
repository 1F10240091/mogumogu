import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-orange-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <section className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">もぐもぐ</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8">
            保育園の献立を活かした家庭の夕食を自動提案します。
            <br />
            離乳食・幼児食のレシピを検索してみましょう。
          </p>
          <Link
            href="/recipes"
            className="inline-flex items-center px-8 py-3 bg-orange-600 text-white font-medium rounded-lg hover:bg-orange-700 transition-colors"
          >
            レシピを探す
          </Link>
        </section>

        <section className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-4xl mx-auto">
          {[
            {
              title: 'かんたん検索',
              description:
                '材料やキーワード、調理時間で絞り込んでお気に入りのレシピを見つけられます。',
            },
            {
              title: 'カテゴリ別',
              description: '主菜・副菜・汁物・ごはんなど、食べたいジャンルから選べます。',
            },
            {
              title: '子ども向け',
              description: '離乳食・幼児食にぴったりの、やさしい味付けのレシピがそろっています。',
            },
          ].map((feature) => (
            <div
              key={feature.title}
              className="bg-white p-6 rounded-xl shadow-sm border border-gray-100"
            >
              <h2 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h2>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </section>
      </div>
    </main>
  );
}
