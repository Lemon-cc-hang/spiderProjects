import requests
import re
from lxml import etree

content_re = re.compile('"excerptArea":{"text":"(.*?)"}')
# "link":{"url":"hstion\u002F388046954"}
url_re = re.compile('"link":{"url":"(.*?)"}')

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.83 Safari/537.36'}


def get_html():
    url = 'https://www.zhihu.com/billboard'
    html = requests.get(url, headers=headers)
    soup = etree.HTML(html.text)  # xpath包装解析
    title = soup.xpath("//a[@class='HotList-item']/div/div[@class='HotList-itemTitle']/text()")
    for t in title:
        print('标题:', t)

    html_text = html.text

    img = soup.xpath("//div[@class='HotList-itemImgContainer']/img/@src")
    for i in img:
        print('img', i)

    contents = content_re.findall(html_text)

    for c in contents:
        print('内容:', c)

    urls = url_re.findall(html_text)

    for url in urls:
        print('url:', url)


if __name__ == '__main__':
    get_html()
