import feedparser

RSS_FEED_URL = "https://blog.goo.ne.jp/shinanren/index.rdf"

def get_latest_article():
    """RSSフィードを解析して最新記事のタイトルとURLを取得する"""
    print("🔍 RSSフィードを取得中...")

    feed = feedparser.parse(RSS_FEED_URL)

    if not feed.entries:
        print("❌ RSSフィードに記事がありません！")
        return None, None

    latest_entry = feed.entries[0]  # 一番最新の記事を取得
    latest_title = latest_entry.title
    latest_link = latest_entry.link

    print(f"✅ 最新記事: {latest_title} ({latest_link})")
    return latest_link, latest_title

def main():
    print("🚀 `script.py` が実行されました！（RSS版）")
    latest_link, latest_title = get_latest_article()
    if latest_link is None:
        print("⚠️ 最新記事が取得できませんでした。スクリプトを終了します。")
        return
    print("🆕 最新記事の情報が取得されました！")

# スクリプト実行
if __name__ == "__main__":
    main()
