from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()
driver.get("https://www.tempo.co/search?q=kurikulum+merdeka&page=2")
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "figure")))

soup = BeautifulSoup(driver.page_source, 'lxml')
articles = soup.find_all('figure')

count = 0
for article in articles:
    if count >= 5:
        break

    try:
        figcaption = article.find('figcaption')
        if not figcaption:
            continue

        a_tag = figcaption.find('a')
        if not a_tag:
            continue

        title = a_tag.text.strip()
        link = "https://www.tempo.co" + a_tag['href']

        # buka link berita
        driver.get(link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(2)

        article_soup = BeautifulSoup(driver.page_source, 'lxml')

        # Ambil tanggal dari <p class="text-neutral-900 text-sm">
        tanggal_tag = article_soup.find('p', class_='text-neutral-900 text-sm')
        date = tanggal_tag.text.strip() if tanggal_tag else 'Tanggal tidak ditemukan'

        # Coba beberapa alternatif lokasi isi konten
        content_div = (
            article_soup.find('div', id='isi') or
            article_soup.find('div', class_='article-content') or
            article_soup.find('article')
        )

        if content_div:
            paragraphs = content_div.find_all('p')
            content = '\n'.join(p.text for p in paragraphs if p.text.strip())
        else:
            content = 'Konten tidak ditemukan'

        # Cetak hasil
        count += 1
        print(f"{count}. Judul   : {title}")
        print(f"   Tanggal : {date}")
        print(f"   Link    : {link}")
        print(f"   Isi     : {content[:300]}...\n{'='*80}\n")

    except Exception as e:
        print("Gagal mengambil data:", e)

driver.quit()
