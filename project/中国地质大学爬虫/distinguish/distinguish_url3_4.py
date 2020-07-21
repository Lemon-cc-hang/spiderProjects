import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


class Get_url3:

    def __init__(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                   'Referer': 'http://grzy.cug.edu.cn/jsjx.jsp?urltype=tree.TreeTempUrl&wbtreeid=1016'}

        self.session = requests.session()
        self.session.headers = headers
        with open('urls/3.txt', 'r')as f:
            self.urls = f.readline().split(',')
        with open('urls/3.txt', 'w')as f:
            pass

    # 获取页面信息
    def get_html(self, url):
        html = self.session.get(url)
        if html.status_code == 200:
            html.encoding = 'utf8'
            self.parse(html.text, url)
        else:
            print(html.status_code)

    # 解析页面, 并用name 来区分是哪一种类型的页面
    # 注意事项, 写入文档是追加形式
    def parse(self, html, url):
        soup = BeautifulSoup(html, 'lxml')
        name = soup.select_one('.t_photo span')

        # print(name)
        if name:
            with open('urls/3.txt', 'a+') as f:
                f.write(url + ',')
        else:
            with open('urls/4.txt', 'a+')as f:
                f.write(url + ',')

    def run(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            [executor.submit(self.get_html, url) for url in self.urls]
