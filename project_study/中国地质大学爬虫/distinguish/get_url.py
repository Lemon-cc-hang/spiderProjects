import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


class Get_url:

    def __init__(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                   'Referer': 'http://grzy.cug.edu.cn/jsjx.jsp?urltype=tree.TreeTempUrl&wbtreeid=1016'}

        self.session = requests.session()
        self.session.headers = headers
        self.urls = ['http://grzy.cug.edu.cn/xyjslb.jsp?totalpage=10&PAGENUM={}&urltype=tsites.CollegeTeacherList&wbtreeid=1012&id=1002&lang=zh_CN'.format(i) for i in range(1, 11)]
        self.teacher_urls = []
        with open('urls/1.txt', 'w')as f:
            pass
        with open('urls/2.txt', 'w')as f:
            pass

    # 请求页面信息
    def get_html(self, url):
        html = self.session.get(url)
        if html.status_code == 200:
            html.encoding = 'utf8'
            return html.text
        else:
            print(html.status_code)

    # 获取url
    def get_url(self, html, url):
        soup = BeautifulSoup(html, 'lxml')
        new_url = soup.select('.clearfix .item')
        for new in new_url:
            u = new.select_one('.inner.clearfix a')['href']
            self.teacher_urls.append(u)

    # 区分第一种类型的页面和其他的, 分别存入
    def parse(self, html, url):
        soup = BeautifulSoup(html, 'lxml')
        name = soup.select_one('.name h1')
        # print(name)
        if name:
            with open('urls/1.txt', 'a+') as f:
                f.write(url + ',')
        else:
            with open('urls/2.txt', 'a+')as f:
                f.write(url + ',')

    # 启动函数 使用多线程
    def run(self):
        for url in self.urls:
            self.get_html(url)
        with ThreadPoolExecutor(max_workers=5) as executor:
            [executor.submit(self.get_url(self.get_html(url), url), url) for url in self.urls]
        with ThreadPoolExecutor(max_workers=5) as executor:
            [executor.submit(self.parse(self.get_html(url), url), url) for url in self.teacher_urls]

