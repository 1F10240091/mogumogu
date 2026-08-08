import Link from "next/link";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <span className={styles.logo}>MoguMogu</span>
          <nav className={styles.nav}>
            <Link href="/recipe-search">レシピ検索</Link>
            <Link href="/login">ログイン</Link>
            <Link href="/register" className={styles.registerLink}>
              新規登録
            </Link>
          </nav>
        </div>
      </header>

      <main className={styles.main}>
        <section className={styles.hero}>
          <h1 className={styles.title}>毎日の夕食づくり、もう悩まない。</h1>
          <p className={styles.subtitle}>
            保育園の献立表を読み取り、アレルギー・好き嫌い・冷蔵庫の在庫を考慮した
            夕食献立を AI が自動提案します。
          </p>
          <Link href="/register" className={styles.cta}>
            はじめる
          </Link>
        </section>

        <section className={styles.features}>
          <h2 className={styles.sectionTitle}>できること</h2>
          <div className={styles.grid}>
            <div className={styles.feature}>
              <h3>献立表の OCR 読み取り</h3>
              <p>保育園から配布された献立表 PDF を読み込み、即座にデジタルデータへ変換。</p>
            </div>
            <div className={styles.feature}>
              <h3>AI 献立自動提案</h3>
              <p>園の昼食と食材が重複せず、在庫を活かした夜ご飯を自動で決定。</p>
            </div>
            <div className={styles.feature}>
              <h3>アレルギー・好き嫌い管理</h3>
              <p>子どもの食事情報を一元管理し、安全でストレスのない食事管理の土台を提供。</p>
            </div>
            <div className={styles.feature}>
              <h3>スマートにお買い物</h3>
              <p>不足食材リストを自動生成し、買い物の負担を削減。</p>
            </div>
          </div>
        </section>
      </main>

      <footer className={styles.footer}>
        <p>MoguMogu — 保育園児の親向け献立自動生成アプリ</p>
      </footer>
    </div>
  );
}
