from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery
import time

KEYWORD = '多肉'
browsers = webdriver.Chrome('D:\\Program Files\\chormedriver\\chromedriver.exe')
wait = WebDriverWait(browsers, 10)
page = 1


def crawl_page(page):
    try:
        url = 'https://s.taobao.com/search?q='+quote(KEYWORD)
        browsers.get(url)
        time.sleep(5)

        if page > 1:
            page_box = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.input.J_Input'))
            )
            btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.J_Submit'))
            )
            page_box.clear()
            page_box.send_keys(page)
            btn.click()

        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item'))
        )
        get_products(page)

    except:
        crawl_page(page)


def get_products(page):
    html = browsers.page_source
    doc = PyQuery(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    filename = '{}_{}.txt'.format(KEYWORD, page)
    with open(filename, 'wb')as f:
        for item in items:
            product = {
                'image' : item.find('img').attr('data-src'),
                'price' : item.find('.price strong').text(),
                'deal': item.find('.deal-cnt').text(),
                'title': item.find('.row.row-2.title').text(),
                'shop': item.find('.shopname').text(),
                'location': item.find('.location').text(),
            }
            print(
                'img:{}\nprice:{}\ndeal:{}\ntitle:{}\nshop{}\nlocation:{}\n\n'.format(product['image'],product['price'],product['deal'],product['title'],product['shop'],product['location'])
            )
            x = 'img:{}\nprice:{}\ndeal:{}\ntitle:{}\nshop{}\nlocation:{}\n\n'.format(product['image'],product['price'],product['deal'],product['title'],product['shop'],product['location'])
            f.write(x.encode('utf-8'))


crawl_page(page)