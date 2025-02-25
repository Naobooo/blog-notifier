import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BLOG_URL = "https://blog.goo.ne.jp/shinanren"

def get_latest_article():
    """Seleniumを使って最新記事のタイトルとリンクを取得する"""
    print("🔍 ブログにアクセス中（Selenium使用）...")

    # Chromeドライバーのセットアップ
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # ヘッドレスモード（画面なし）
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # ブログページを開く
        driver.get(BLOG_URL)
        time.sleep(5)  # 読み込み待機

        print("✅ ページの読み込み完了！")

        # 最新記事のリンクを取得（XPathを修正）
        latest_article = driver.find_element(By.XPATH, '//div[contains(@class, "entry")]//h2[contains(@class, "title")]/a')
        latest_title = latest_article.text
        latest_link = latest_article.get_attribute("href")

        print(f"✅ 最新記事: {latest_title} ({latest_link})")
        return latest_link, latest_title

    except Exception as e:
        print(f"❌ 記事の取得中にエラーが発生: {e}")
        return None, None

    finally:
        driver.quit()  # ドライバーを終了

def main():
    print("🚀 `script.py` が実行されました！（Selenium版）")
    latest_link, latest_title = get_latest_article()
    if latest_link is None:
        print("⚠️ 最新記事が取得できませんでした。スクリプトを終了します。")
        return
    print("🆕 最新記事の情報が取得されました！")

# スクリプト実行
if __name__ == "__main__":
    main()

