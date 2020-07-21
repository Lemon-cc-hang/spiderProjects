import requests
from bs4 import BeautifulSoup
import random

links = ["http://guba.eastmoney.com/"]
url = "http://guba.eastmoney.com/"

def page_get_link(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.83 Safari/537.36'}
    html = requests.get(url, headers=headers)
    bso = BeautifulSoup(html.text,'html.parser')
    for link in bso.select('a'):
        if "href" in link.attrs:
            print(link.attrs['href'])
            links.append(link.attrs['href'])

while len(links) > 0:
    links = [link for link in links if link is not None and 'http' in link]    # 很牛逼的东西
    new_url = links[random.randint(0, len(links)-1)]
    page_get_link(new_url)
    print(links)
