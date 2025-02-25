import feedparser
import requests
import os

RSS_FEED_URL = "https://blog.goo.ne.jp/shinanren/index.rdf"

# 環境変数からLINE APIの設定を取得
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")  # 送信先ユーザーID

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

def send_line_message(message):
    """LINEに通知を送る"""
    if not LINE_ACCESS_TOKEN:
        print("❌ LINE_ACCESS_TOKEN が設定されていません！")
        return
    if not LINE_USER_ID:
        print("❌ LINE_USER_ID が設定されていません！")
        return

    print(f"📩 送信先LINE_USER_ID: {LINE_USER_ID}")  # デバッグ用

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message}]
    }

    response = requests.post(url, json=data, headers=headers)
    print(f"✅ LINE API のレスポンス: {response.status_code} {response.text}")

    if response.status_code != 200:
        print("❌ LINE通知に失敗しました！")
        print(f"レスポンス: {response.text}")

def main():
    print("🚀 `script.py` が実行されました！（RSS + LINE通知版）")
    latest_link, latest_title = get_latest_article()
    if latest_link is None:
        print("⚠️ 最新記事が取得できませんでした。スクリプトを終了します。")
        return

    message = f"🆕 新しい記事が投稿されました！\n📌 {latest_title}\n🔗 {latest_link}"
    send_line_message(message)

    print("✅ LINE通知が送信されました！")

# スクリプト実行
if __name__ == "__main__":
    main()
