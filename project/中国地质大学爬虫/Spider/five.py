import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


class FiveSpider:
    def __init__(self, store):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                   'Referer': 'http://grzy.cug.edu.cn/jsjx.jsp?urltype=tree.TreeTempUrl&wbtreeid=1016'}

        self.session = requests.session()
        self.session.headers = headers
        self.urls = ['http://grzy.cug.edu.cn/luobiji/zh_CN/index.htm', 'http://grzy.cug.edu.cn/pengsongbo/zh_CN/index.htm']
        self.store = store

    def get_html(self, url):
        html = self.session.get(url)
        if html.status_code == 200:
            html.encoding = 'utf8'
            return html.text
        else:
            print(html.status_code)

    def parse(self, html, url):
        try:
            soup = BeautifulSoup(html, 'lxml')
            name = soup.select_one('.namebar.clearfix h2').text.strip()
            zhiCheng = soup.select('.zw')[0].text.strip()
            content = soup.select('.baseinfobar .ct p')
            time = None
            graduateSchool = None
            gender = None
            subject = None
            for c in content:
                r = c.text.strip().split('\n')
                for r1 in r:
                    if r1:
                        r2 = r1.strip().split('：')
                        # print(r2)
                        if r2[0].strip() == '入职时间':
                            time = r2[1]
                        if r2[0].strip() == '毕业院校':
                            graduateSchool = r2[1]
                        if r2[0].strip() == '性别':
                            gender = r2[1]
                        if r2[0].strip() == '学科':
                            subject = r2[1]
            # print('-'*50)
            # print(time, graduateSchool, gender, subject)
            # # print(zhiCheng)
            url_xmxx = 'http://grzy.cug.edu.cn/' + soup.select('#MenuBar1 li div div a')[1]['href']
            url_lwcg = 'http://grzy.cug.edu.cn/' + soup.select('#MenuBar1 li div div a')[4]['href']
            # print(url_xmxx)
            # print(url_lwcg)
            soup_xmxx = BeautifulSoup(self.get_html(url_xmxx), 'lxml')
            xmxx = ""
            # print(xmxx)
            soup_lwcg = BeautifulSoup(self.get_html(url_lwcg), 'lxml')
            content = soup_lwcg.select('.clearfix a h2')
            lwcg = ""
            for c in content:
                lwcg += ('- ' + c.text.strip() + '\n')
            # print(lwcg)
            self.store.count += 1
            self.store.sheet.write(self.store.count, 0, self.store.count)
            self.store.sheet.write(self.store.count, 1, name)
            self.store.sheet.write(self.store.count, 2, time)
            self.store.sheet.write(self.store.count, 3, zhiCheng)
            self.store.sheet.write(self.store.count, 4, graduateSchool)
            self.store.sheet.write(self.store.count, 5, gender)
            self.store.sheet.write(self.store.count, 6, subject)
            self.store.sheet.write(self.store.count, 7, xmxx)
            self.store.sheet.write(self.store.count, 8, lwcg)
            self.store.sheet.write(self.store.count, 9, url)
        except:
            pass

    def run(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            [executor.submit(self.parse(self.get_html(url), url), url) for url in self.urls]
        # self.Excel_book.save('data.xls')

