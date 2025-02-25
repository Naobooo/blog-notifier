import requests
from bs4 import BeautifulSoup
import os

BLOG_URL = "https://blog.goo.ne.jp/shinanren"

# User-Agent を変更し、Referer を設定
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.google.com/"
}

def get_latest_article():
    """最新記事のタイトルとリンクを取得する"""
    print("🔍 ブログにアクセス中...")
    
    # セッションを使用して Cookie を維持
    session = requests.Session()
    response = session.get(BLOG_URL, headers=HEADERS)
    
    print(f"✅ HTTPステータスコード: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ ブログにアクセスできません！（ステータスコード: {response.status_code}）")
        return None, None

    soup = BeautifulSoup(response.text, "html.parser")

    print("🔍 取得したHTMLの一部:")
    print(soup.prettify()[:1000])  # 最初の1000文字だけ出力（長すぎるとGitHub Actionsのログに影響）

    # 記事リストの div を探す（新しいクラス名に変更）
    article = soup.find("div", class_="entry")
    if article is None:
        print("❌ ブログのHTML構造が変更された可能性があります！（`div.entry` が見つかりません）")
        return None, None

    # 記事のタイトルリンクを取得
    link_tag = article.find("h2", class_="title").find("a")
    if link_tag is None:
        print("❌ 記事のリンクが見つかりません！（`h2.title > a` が見つかりません）")
        return None, None

    latest_link = link_tag["href"]
    latest_title = link_tag.text.strip()

    print(f"✅ 最新記事: {latest_title} ({latest_link})")
    return latest_link, latest_title

def main():
    print("🚀 `script.py` が実行されました！")
    latest_link, latest_title = get_latest_article()
    if latest_link is None:
        print("⚠️ 最新記事が取得できませんでした。スクリプトを終了します。")
        return
    print("🆕 最新記事の情報が取得されました！")

# スクリプト実行
if __name__ == "__main__":
    main()

