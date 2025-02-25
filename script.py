import requests
from bs4 import BeautifulSoup
import os

# gooブログのURL
BLOG_URL = "https://blog.goo.ne.jp/shinanren"

# LINE Messaging API のアクセストークン（GitHub Secrets から取得）
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")

# 送信先の LINE ユーザー ID または グループ ID
LINE_TO = os.getenv("LINE_TO")

def get_latest_article():
    """ 最新記事のタイトルとリンクを取得する """
    response = requests.get(BLOG_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # 最新記事の取得（ブログのHTML構造に合わせて変更する）
    article = soup.find("div", class_="entrylist").find("a")
    latest_link = article["href"]
    latest_title = article.text.strip()

    return latest_link, latest_title

def send_line_message(message):
    """ LINEグループにメッセージを送る """
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "to": LINE_TO,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post(url, json=data, headers=headers)

def check_and_notify():
    """ 記事をチェックして更新があれば通知を送る """
    latest_link, latest_title = get_latest_article()
    send_line_message(f"🆕 新しい記事が投稿されました！\n📌 {latest_title}\n🔗 {latest_link}")

# スクリプト実行
check_and_notify()
