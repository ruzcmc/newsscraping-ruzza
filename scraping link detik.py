import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

base_url = "https://www.detik.com/search/searchnews"
query = "ruu tni"
from_date = "01/01/2025"
to_date = "26/03/2025"
result_type = "latest"

page = 1
all_links = []

while True:
    params = {
        "query": query,
        "page": page,
        "result_type": result_type,
        "fromdatex": from_date,
        "todatex": to_date
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page}")
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')

    if not articles:
        print(f"No more articles found on page {page}. Stopping.")
        break

    for article in articles:
        link = article.find('a', href=True)
        if link:
            all_links.append(link['href'])

    print(f"Page {page} processed.")
    page += 1
    time.sleep(1)  # Be respectful and avoid overwhelming the server

# Output all collected links
for idx, link in enumerate(all_links, 1):
    print(f'"{link}",')
#df = pd.DataFrame(all_links, columns=['links'])
#df.to_csv('list link detik.csv')