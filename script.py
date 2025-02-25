import requests
from bs4 import BeautifulSoup

BLOG_URL = "https://blog.goo.ne.jp/shinanren"

def get_latest_article():
    """ 最新記事のタイトルとリンクを取得する """
    response = requests.get(BLOG_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    print("🔍 取得したHTMLの一部:")
    print(soup.prettify())  # ← HTMLをログに出力

    # 記事リストの div を探す（HTML構造に合わせて変更）
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


