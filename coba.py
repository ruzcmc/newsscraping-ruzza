import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def ambil_detail_berita(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")

        # Ambil judul
        judul_tag = soup.find("h1")
        judul = judul_tag.get_text(strip=True) if judul_tag else ""

        # Ambil isi artikel
        isi_paragraf = soup.find_all("p")
        isi_berita = "\n".join(p.get_text(strip=True) for p in isi_paragraf)

        return judul, isi_berita
    except Exception as e:
        print(f"❌ Gagal ambil {url}: {e}")
        return "", ""

def scrape_semua_halaman(max_page=62):
    base_url = "https://search.kompas.com/search?q=pilpres&site_id=all&start_date=2018-01-01&end_date=2019-05-01&page={}"
    data_berita = []
    
    

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        # Add other headers as needed
    }

    for page in range(1, max_page + 1):
        print(f"\n🔎 Scraping halaman {page}...")
        res = requests.get(base_url.format(page), headers=headers)
        soup = BeautifulSoup(res.content, "html.parser")

        article_items = soup.find_all("div", class_="articleItem")

        for idx, item in enumerate(article_items, 1):
            a_tag = item.find("a", class_="article-link")
            tgl_tag = item.find("div", class_="articlePost-date")

            if a_tag:
                link = a_tag['href']
                tanggal = tgl_tag.get_text(strip=True) if tgl_tag else "Tidak ada tanggal"

                judul, isi = ambil_detail_berita(link)
                data_berita.append({
                    "URL": link,
                    "Tanggal": tanggal,
                    "Judul": judul,
                    "Isi Berita": isi
                })

                print(f"✅ Artikel ke-{idx} di halaman {page} berhasil diambil.")
                time.sleep(1)  # Hindari beban server

    print(data_berita[0])
    # Simpan ke Excel
    #df = pd.DataFrame(data_berita)
    #df.to_excel("kompas_pilpres20182019.xlsx", index=False)
    #print(f"\n📁 Data berhasil disimpan ke dengan {len(df)} artikel.")

if __name__ == "__main__":
    scrape_semua_halaman()