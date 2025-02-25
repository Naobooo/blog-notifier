import requests
from bs4 import BeautifulSoup
import os
import time

BLOG_URL = "https://blog.goo.ne.jp/shinanren"

# User-Agent を変更し、Referer を設定（ブラウザ経由を装う）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Referer": "https://www.google.com/",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8"
}

def get_latest_article():
    """最新記事のタイトルとリンクを取得する（リトライ機能付き）"""
    print("🔍 ブログにアクセス中...")

    session = requests.Session()
    session.headers.update(HEADERS)

    for attempt in range(3):  # 3回までリトライ
        try:
            response = session.get(BLOG_URL)
            print(f"✅ HTTPステータスコード: {response.status_code}")

            if response.status_code == 200:
                break  # 成功したらループを抜ける
            else:
                print(f"⚠️ ステータスコード: {response.status_code}。5秒待機して再試行します...")
                time.sleep(5)
        except requests.exceptions.RequestException as e:
            print(f"❌ リクエストエラー: {e}")
            time.sleep(5)

    if response.status_code != 200:
        print("❌ すべてのリトライに失敗しました。")
        return None, None

    soup = BeautifulSoup(response.text, "html.parser")
    print("🔍 取得したHTMLの一部:")
    print(soup.prettify()[:1000])  # 最初の1000文字だけ出力

    # 記事リストの div を探す（正しいクラス名に修正）
    article_list = soup.find("div", class_="blog_index_list")
    if article_list is None:
        print("❌ 記事リストが見つかりません！（`div.blog_index_list` が見つからない）")
        return None, None

    # 記事のタイトルリンクを取得
    link_tag = article_list.find("div", class_="blog_index_title").find("a")
    if link_tag is None:
        print("❌ 記事のリンクが見つかりません！（`div.blog_index_title > a` が見つからない）")
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

if __name__ == "__main__":
    main()
