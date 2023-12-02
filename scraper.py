import requests
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

def exist(typ, _class, soup): # used to check if an element exists
    it = soup.find(typ, _class)
    if it is not None: return True
    return False

def load_old_offers(file):
    # used to load offers that already exist in db, so we have as little duplicates as possible
    offers = set() # use set because of time complexity
    with open(file, 'r') as f:
        for r in f:
            offers.add(r)
    return offers

def get_new_offers(session, start_page, last_page, old_offers):
    # load new offers, check if they already exist in file using set 
    # save new offers into the file
    # return "OFFERS" which contains only newly added offers a
    # print the number of all new listings that were added
    
    OFFERS = []
    with open('offers.txt', 'a+') as ofs:
        for i in range(start_page, last_page+1):
            listings = session.get(f'{URL}&page={i}', headers=HEADERS, proxies={"http": random.choice(PROXIES)})
            if listings.status_code==200:
                print(f'Page {i} loaded successfully.')
                soup = bs(listings.text, 'html.parser')
                links = soup.find_all('a',  {'data-cy':'listing-item-link'}) # find by class didnt work for some reason
                hrefs = [link.get('href') for link in links]
                for r in hrefs:
                    if r not in old_offers:
                        print(r, file=ofs)
                        old_offers.add(r)
                        OFFERS.append(r)
            else:
                print(f'Failed to load page {i}. Error code: {listings.status_code}')
            sleep(random.uniform(0.75, 1.6))

    print(f"Loading new offers finished successfully. There's {len(OFFERS)} new offers.")
    return OFFERS

def get_details(OFFERS, session, output_file):
    # for each href in OFFERS fetch details and save in output_file
    # save idx in last_checked.txt to avoid fetching the same offer more than once
    with open('last_checked.txt', 'r') as lc:
        idx = lc.readline().strip()
        if idx=='':
            idx = 0
        else:
            idx = int(idx)

    OFFERS = list(OFFERS)
    while idx<len(OFFERS):
        ref = OFFERS[idx].strip()
        detailed = session.get(f'{ROOT}{ref}', headers=HEADERS, proxies={'http': random.choice(PROXIES)})
        if detailed.status_code!=200:
            print(f'Failed to load page {ROOT}{ref}. Error code: {detailed.status_code}')
        else:
            print(f'{idx}/{len(OFFERS)}')
            # get detailed data about listing
            # checking if values exist is crucial so the code wont crash
            soup = bs(detailed.content, 'html.parser')
            location = soup.find('a', {'class':'e1w8sadu0 css-1helwne exgq9l20'}).text.strip() if exist('a', {'class':'e1w8sadu0 css-1helwne exgq9l20'}, soup) else ''
            total_price = soup.find('strong', {'class': 'css-t3wmkv e1l1avn10'}).text.strip() if exist('strong', {'class': 'css-t3wmkv e1l1avn10'}, soup) else ''
            price_per_sqm = soup.find('div', {'class':'css-1h1l5lm efcnut39'}).text.strip() if exist('div', {'class':'css-1h1l5lm efcnut39'}, soup) else ''
            area = soup.find('div', {'class':'css-1wi2w6s enb64yk5'}).text.strip() if exist('div', {'class':'css-1wi2w6s enb64yk5'}, soup) else ''
            rooms = soup.find('div', {'class': 'css-1wi2w6s', 'data-testid': 'table-value-rooms_num'}).text.strip() if exist('div', {'class': 'css-1wi2w6s', 'data-testid': 'table-value-rooms_num'}, soup) else ''
            finished = soup.find('div', {'class': 'css-kkaknb enb64yk1', 'aria-label': 'Stan wykończenia', 'role': 'region'}).text.strip()[16:] if exist('div', {'class': 'css-kkaknb enb64yk1', 'aria-label': 'Stan wykończenia', 'role': 'region'}, soup) else ''
            floor = soup.find('div', {'class': 'css-1wi2w6s enb64yk5', 'data-testid': 'table-value-floor'}).text.strip() if exist('div', {'class': 'css-1wi2w6s enb64yk5', 'data-testid': 'table-value-floor'}, soup) else ''
            outside = soup.find('div', {'class':'css-1wi2w6s enb64yk5', 'data-testid': 'table-value-outdoor'}).text.strip() if exist('div', {'class':'css-1wi2w6s enb64yk5', 'data-testid': 'table-value-outdoor'}, soup) else ''
            rent = soup.find('div', {'data-testid':'table-value-rent', 'class': 'css-1wi2w6s enb64yk5'}).text.strip() if exist('div', {'data-testid':'table-value-rent', 'class': 'css-1wi2w6s enb64yk5'}, soup) else ''
            elevator = soup.find('div', {'data-testid':'table-value-lift', 'class': 'css-1wi2w6s enb64yk5'}).text.strip() if exist('div', {'data-testid':'table-value-lift', 'class': 'css-1wi2w6s enb64yk5'}, soup) else ''
            built = soup.find('div', {'data-testid':'table-value-build_year', 'class': 'css-1wi2w6s enb64yk5'}).text.strip() if exist('div', {'data-testid':'table-value-build_year', 'class': 'css-1wi2w6s enb64yk5'}, soup) else ''
            b_type = soup.find('div', {'data-testid':'table-value-building_type', 'class': 'css-1wi2w6s enb64yk5'}).text.strip() if exist('div', {'data-testid':'table-value-building_type', 'class': 'css-1wi2w6s enb64yk5'}, soup) else ''
            row = f'{location};{total_price};{price_per_sqm};{area};{rooms};{finished};{floor};{outside};{rent};{elevator};{built};{b_type};{ROOT}{ref}'
            with open(output_file, 'a+') as dets:
                print(row, file=dets)
        idx += 1
        with open('last_checked.txt', 'w') as lc:
            print(idx, file=lc)
        sleep(random.uniform(0.5, 1.25))

    print('Process finished successfully.')
    with open('last_checked.txt', 'w') as lc: # clear last_checked only after completing the task
        print(0, file=lc)

def main():
    session = requests.Session()
    old = load_old_offers('offers.txt')
    OFFERS = get_new_offers(session, 151, 250, old)
    get_details(OFFERS, session, 'details.txt')

main()