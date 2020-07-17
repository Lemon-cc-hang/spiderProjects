import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.83 Safari/537.36'}


def math(text):
    text = text.encode('utf-8')
    text = text.replace(b'\xee\x86\xa9', b'0')
    text = text.replace(b'\xee\x97\xbd', b'1')
    text = text.replace(b'\xef\x81\xbc', b'2')
    text = text.replace(b'\xef\x9d\xab', b'3')
    text = text.replace(b'\xee\xb3\x8d', b'4')
    text = text.replace(b'\xee\x80\x8d', b'5')
    # text = text.replace(b'\xee\x86\xa9', b'6')
    # text = text.replace(b'\xee\x86\xa9', b'7')
    text = text.replace(b'\xef\xa0\xb5', b'8')
    text = text.decode()
    return text

for page in range(1,2):
    html = requests.get('https://www.shixiseng.com/interns?page={}'.format(page),headers=headers)

    soup = BeautifulSoup(html.text, 'lxml')
    filename = 'shixiseng_{}.txt'.format(page)
    with open(filename, 'wb')as f:
        datas = soup.select('.intern-wrap.intern-item')
        for data in datas:
            title = data.select('.title.font')[0].text
            price = data.select('.day.font')[0].text
            price = math(price)
            place = data.select('.city.ellipsis')[0].text

            print('title:{}\nprice:{}\nplace:{}\n\n'.format(title, price, place))
            f.write('title:{}\nprice:{}\nplace:{}\n\n'.format(title, price, place).encode('utf-8'))