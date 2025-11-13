#isok tambahi timeout exception
import requests
import xml.etree.ElementTree as ET
from selenium import webdriver
#from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from bs4 import BeautifulSoup
#from tqdm.notebook import tqdm
from tqdm import tqdm


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',}
        # Add other headers as needed
# Inisialisasi driver
#chrome_options = Options()
#chrome_options.add_argument("--start-maximized")
#chrome_options.add_argument("--headless")  # uncomment kalau mau headless


profile = FirefoxProfile("C:\\Users\\Ruzza\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\jrad7wfv.selenium")
# Use the above folder as custom profile
opts = Options()
opts.add_argument("-binary_location")
opts.add_argument("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
opts.add_argument("--headless")
opts.profile = profile


driver = webdriver.Firefox(options=opts)



# Simpan data di list
data_berita = []

# Loop halaman 1 - 100
#dikasih try jika ga ada harus break
for page in range(1, 350):
    print(f" Scraping halaman {page}...")
    url = f"https://www.cnnindonesia.com/search?query=ma'ruf+amin&result_type=latest&fromdate=17/04/2018&todate=17/04/2019&page={page}"
    
    while True:
        try:
            driver.get(url)
            time.sleep(5)
            break
        except Exception as e:
            print ("reloading: because exception ",e)
            continue  # tunggu konten muncul

    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = soup.find_all("article", class_="flex-grow")

    for article in tqdm(articles):
        a_tag = article.find("a")
        if not a_tag:
            continue

        h2 = a_tag.find("h2")
        tanggal_span = a_tag.find("span", class_="text-cnn_black_light3")

        if not h2 or not tanggal_span:
            continue

        judul = h2.get_text(strip=True)
        print("scraping",judul)
        tanggal = tanggal_span.get_text(strip=True)
        link = a_tag["href"]

        # Ambil isi artikel
        try:
            res = requests.get(link, headers=headers)
            artikel_soup = BeautifulSoup(res.text, "html.parser")

            # Ambil tanggal dari dalam artikel
            tanggal_div = artikel_soup.find("div", class_="text-cnn_grey text-sm mb-4")
            tanggal = tanggal_div.get_text(strip=True) if tanggal_div else "Tanggal tidak ditemukan"

            # Ambil isi berita
            konten = artikel_soup.find("div", class_="detail-text")
            isi_berita = ""
            if konten:
                paragraphs = konten.find_all("p")
                isi_berita = " ".join(p.get_text(strip=True) for p in paragraphs)

            # Tambahkan ke list
            data_berita.append({
                "Judul": judul,
                "Tanggal": tanggal,
                "Link": link,
                "Isi Berita": isi_berita
            })

        except Exception as e:
            print(f" Gagal ambil isi dari {link} karena {e}")
    if page % 10 == 0:
        df_temp = pd.DataFrame(data_berita)
        df_temp.to_csv(f"D:\\scraping\\manualscraping\\CNN_currentstate.csv", index=False)

driver.quit()

# Simpan ke Excel
df = pd.DataFrame(data_berita)
#df.sample(n=5)
df.to_csv("D:\\scraping\\manualscraping\\CNN_marufamin2019.csv", index=False)
#print("✅ Selesai! Data disimpan ke 'CNN_Kurikulum Merdeka.xlsx'")