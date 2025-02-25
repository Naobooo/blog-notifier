import requests
from bs4 import BeautifulSoup
import os

BLOG_URL = "https://blog.goo.ne.jp/shinanren"

LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_TO = os.getenv("LINE_TO")

def get_latest_article():
    """ 最新記事のタイトルとリンクを取得する """
    print("🔍 ブログにアクセス中...")
    response = requests.get(BLOG_URL)
    print(f"✅ HTTPステータスコード: {response.status_code}")

    if response.status_code != 200:
        raise ValueError(f"❌ ブログにアクセスできません！（ステータスコード: {response.status_code}）")

    soup = BeautifulSoup(response.text, "html.parser")

    print("🔍 取得したHTMLの一部:")
    print(soup.prettify()[:1000])  # 最初の1000文字だけ出力（長すぎるとGitHub Actionsのログに影響）

    # 記事リストの div を探す
    article_list = soup.find("div", class_="blog_index_main")
    if article_list is None:
        raise ValueError("❌ ブログのHTML構造が変更された可能性があります！")

    # 記事のリンクを探す
    link_tag = article_list.find("div", class_="blog_index_title").find("a")
    if link_tag is None:
        raise ValueError("❌ 記事のリンクが見つかりません！")

    latest_link = link_tag["href"]
    latest_title = link_tag.text.strip()

    print(f"✅ 最新記事: {latest_title} ({latest_link})")
    return latest_link, latest_title

def send_line_message(message):
    """LINEに通知を送る"""
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "to": LINE_TO,
        "messages": [{"type": "text", "text": message}]
    }

    response = requests.post(url, json=data, headers=headers)
    print(f"✅ LINE API のレスポンス: {response.status_code} {response.text}")

    if response.status_code != 200:
        print("❌ LINE通知に失敗しました！")
        print(f"レスポンス: {response.text}")

def check_and_notify():
    print("🔍 最新記事のチェックを開始します...")
    latest_link, latest_title = get_latest_article()
    if latest_link is None:
        return

    # 以前の最新記事のURLと比較する（GitHub Actionsは一時的な環境なのでファイルは使えない）
    last_link = os.getenv("LAST_ARTICLE")
    if last_link == latest_link:
        print("✅ 新しい記事はありません。通知しません。")
        return

    print("🆕 新しい記事が投稿されたので通知を送ります！")
    send_line_message(f"🆕 新しい記事が投稿されました！\n📌 {latest_title}\n🔗 {latest_link}")

    # GitHub Actions の環境変数として保存
    os.environ["LAST_ARTICLE"] = latest_link

# スクリプト実行
check_and_notify()
