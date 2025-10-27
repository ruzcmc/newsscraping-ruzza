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
        'Accept-Language': 'en-US,en;q=0.9',
        # Add other headers as needed
    }

def cnn_search(query,before,after):
    url = f"https://www.cnnindonesia.com/search?query=pilpres&result_type=latest&fromdate=14/02/2023&todate=14/02/2024&page={page}"




def gnews_rss(query,before,after): #hanya 100 return max, execute harus in the loop dgn iterasi dan combine all links ke 1 list besar untuk di scrape
    """
    Scrape Google News RSS for a query.
    Args:
        query: search keyword, e.g. "gibran"
        after before: YYYY-MM-DD
    Returns:
        List of article links
    """
    # Construct query
    #https://news.google.com/rss/search?q=intitle%3Agibran%20before%3A2024-02-15%20after%3A2023-02-14%20site%3Ainews.id&hl=id&gl=ID&ceid=ID%3Aid
    url = f"https://news.google.com/rss/search?q=intitle%3A{query}%20before%3A{before}%20after%3A{after}%20site%3Ainews.id&hl=id&gl=ID&ceid=ID%3Aid"
    print(url)
    # Fetch the RSS feed
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    # Parse XML
    root = ET.fromstring(res.text)
    links = []

    for item in root.findall(".//item"):
        link = item.find("link")
        if link is not None:
            links.append(link.text.strip())

    return links

def ambil_detail_berita(url): #gaiso, harus di emulate selenium dulu
    try:
        
    
        #driver.maximize_window()
   
    
        driver.get(url)
        #driver.implicitly_wait(15)  # tunggu konten muncul
        #wait = WebDriverWait(driver, timeout=15)
        #wait.until(EC.url_contains("inews.id"))
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
    
        # Ambil judul
        judul_tag = soup.find("h1")
        judul = judul_tag.get_text(strip=True) if judul_tag else ""

            #time
        time_tag = soup.find("div", class_="createdAt")
        tanggal = time_tag.get_text(strip=True) if time_tag else ""
            

        # Ambil isi artikel
        isi_paragraf = soup.find_all("p")
        isi_berita = "\n".join(p.get_text(strip=True) for p in isi_paragraf)
        #driver.quit()
        return (driver.current_url, tanggal, judul, isi_berita)
        
    except Exception as e:
        print(f" Gagal ambil {url}: {e}")
        return ("", "","","")



#print(gnews_rss("gibran","2024-02-15","2023-02-13"))
#print(ambil_detail_berita("https://news.google.com/rss/articles/CBMirgFBVV95cUxNRzlkOHAtQk45SFBpRnNfNkVwR2tab1JYYUdHNkd3VE1rSm9MR2wyQzE5amJVVThJdkpDTjg2el9XNV9rWW0wVlVWTndFMHIwOTVBaEQtZC0zTDNxTlhyQUxQTV9WV2RxR2p2aS0ycFhpenhJd1MzNHQ1em9OclhjZXBRVGpqSUJQOHUxVnZ5S0dPRWphUkI1U2k3WVg2RUt3YVJNRGU2WWU1Q1NyOHfSAa4BQVVfeXFMT3RxYVYzTjRubC15WFl5RmNMTURZLUtwQU1CYjNlWjJsSHd0Z2NfNGxlU2pISGtENDFoRWpNaFpXWDA4b0VJejczc2toSlFicW5vU2lDcFBpOTlaTDQzdi1oS3ZsaDdnNm1fVmdqaEhLcGVmVHBleUk3OFd3S003V3pzWG5ma1d4MWk2N2ZfZUZ4X3dqbUlFaDNNUzVTaGU3ZzM1cUdwR3RYa3ZVX0l3?oc=5"))
searchterm ="jokowi"
listqueries = [(searchterm,"2024-02-14","2023-11-14"),(searchterm,"2023-11-14","2023-08-14"),(searchterm,"2023-08-14","2023-05-14"),(searchterm,"2023-05-14","2023-02-14")]
#listqueries = [(searchterm,"2019-04-17","2019-01-17"),(searchterm,"2019-01-17","2018-10-17"),(searchterm,"2018-10-17","2018-07-17"),(searchterm,"2018-07-17","2018-04-17")]


links = []
for i in listqueries:
    a = gnews_rss(i[0],i[1],i[2])
    links.extend(a)
#print(links)
#print(len(links))
hasil = []
for y in tqdm(links):
    profile = FirefoxProfile("C:\\Users\\Ruzza\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\jrad7wfv.selenium")
# Use the above folder as custom profile
    opts = Options()
    opts.add_argument("-binary_location")
    opts.add_argument("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
    opts.add_argument("--headless")
    opts.profile = profile
    
    while True:
        try:
            driver = webdriver.Firefox(options=opts)
        except Exception as e:
            print(e)
            continue
        break

    b = ambil_detail_berita(y)
    if b:
        print("scraping:", b[2])
        hasil.append({
            "url":b[0],
            "tanggal":b[1],
            "judul":b[2],
            "isi":b[3]})
    else:
        continue
    driver.quit()
#print(hasil)

df = pd.DataFrame(hasil)
df.to_csv("D:\\scraping\\manualscraping\\inews_google_jokowi2024.csv", index=False)
print(len(df), "scraped")