import requests
import json
import os
from time import *
import random
from bs4 import BeautifulSoup as bs

ROOT = 'https://www.otodom.pl'
URL = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?viewType=listing'

HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Content-Encoding": "gzip",
  "Content-Type": "text/html; charset=utf-8",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
  "Sec-Ch-Ua": "\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

PROXIES = ["50.200.12.82:80", "50.170.90.24:80", "157.245.97.60:80", "80.13.43.193:80", "207.180.249.153:3128", "173.212.250.16:37712", "185.162.229.215:80"]

# get all listings and gather links to details of each listing
session = requests.Session()
OFFERS = []
with open('offers.txt', 'r') as ofs:
    if os.path.getsize('offers.txt')!=0:
        empty = False
        for row in ofs:
            OFFERS.append(row)
    else:
        empty = True
if empty:
    with open('offers.txt', 'w') as ofs:
        for i in range(1, 301): # get 300 pages
            listings = session.get(f'{URL}&page={i}', headers=HEADERS, proxies={"http": random.choice(PROXIES)})
            if listings.status_code==200:
                soup = bs(listings.text, 'html.parser')
                print(i)
                links = soup.find_all('a', class_='css-1hfdwlm e1dfeild2')
                hrefs = [link.get('href') for link in links]
                for r in hrefs:
                    print(r, file=ofs)
                    OFFERS.append(r)
            else:
                print(f'Failed to get page {i}')
            sleep(random.uniform(1,3))

# visit all offers and grab detailed data
# since it can be a long process remember index of link that was visited last
with open('last_checked.txt') as lc:
    idx = int(lc.readline().strip())

while idx<len(OFFERS):
    ref = OFFERS[idx].strip()
    detailed = session.get(f'{ROOT}{ref}', headers=HEADERS, proxies={'http': random.choice(PROXIES)})
    print(f'{ROOT}{ref}')
    if detailed.status_code!=200:
        print(detailed.status_code)
        print(f'Failed to load page {idx}')
    else:
        print(idx)
        # sprawdzanie czy wartosc istnieje
        soup = bs(detailed.content, 'html.parser')
        location = soup.find('a', class_='e1w8sadu0 css-1helwne exgq9l20').text.strip()
        total_price = soup.find('strong', class_='css-t3wmkv e1l1avn10').text.strip()
        price_per_sqm = soup.find('div', class_='css-1h1l5lm efcnut39').text.strip()
        area = soup.find('div', class_='css-1wi2w6s enb64yk5').text.strip()
        rooms = soup.find('div', {'class': 'css-1wi2w6s', 'data-testid': 'table-value-rooms_num'}).text.strip()
        finished = soup.find('div', {'class': 'css-kkaknb enb64yk1', 'aria-label': 'Stan wykończenia', 'role': 'region'}).text.strip()[16:]
        floor = soup.find('div', {'class': 'css-1wi2w6s enb64yk5', 'data-testid': 'table-value-floor'}).text.strip()
        outside = soup.find('div', {'class':'css-1wi2w6s enb64yk5', 'data-testid': 'table-value-outdoor'}).text.strip()
        #xddd
    # save last index checked
    idx += 1
    lc = open('last_checked.txt', 'w')
    print(idx, file=lc)
    lc.close()
    sleep(random.uniform(1, 3))
