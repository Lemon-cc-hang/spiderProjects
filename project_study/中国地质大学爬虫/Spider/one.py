
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


class OneSpider:
    def __init__(self, store):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                   'Referer': 'http://grzy.cug.edu.cn/jsjx.jsp?urltype=tree.TreeTempUrl&wbtreeid=1016'}

        self.session = requests.session()
        self.session.headers = headers
        self.urls = ['http://grzy.cug.edu.cn/caoyi/zh_CN/index.htm', 'http://grzy.cug.edu.cn/gusongzhu/zh_CN/index.htm', 'http://grzy.cug.edu.cn/guojl/zh_CN/index.htm', 'http://grzy.cug.edu.cn/hanfenglu/zh_CN/index.htm', 'http://grzy.cug.edu.cn/Huang_Chunju/zh_CN/index.htm', 'http://grzy.cug.edu.cn/LiHui/zh_CN/index.htm', 'http://grzy.cug.edu.cn/liujinling/zh_CN/index.htm', 'http://grzy.cug.edu.cn/maqiang/zh_CN/index.htm', 'http://grzy.cug.edu.cn/pingxianquan/zh_CN/index.htm', 'http://grzy.cug.edu.cn/songhaijun/zh_CN/index.htm', 'http://grzy.cug.edu.cn/wangdun/zh_CN/index.htm', 'http://grzy.cug.edu.cn/wanglianxun/zh_CN/index.htm', 'http://grzy.cug.edu.cn/wangzaicong/zh_CN/index.htm', 'http://grzy.cug.edu.cn/xuchang/zh_CN/index.htm', 'http://grzy.cug.edu.cn/xiaolong/zh_CN/index.htm', 'http://grzy.cug.edu.cn/xieshucheng/zh_CN/index.htm', 'http://grzy.cug.edu.cn/xuhaijin/zh_CN/index.htm', 'http://grzy.cug.edu.cn/xuyajun/zh_CN/index.htm', 'http://grzy.cug.edu.cn/yansen/zh_CN/index.htm', 'http://grzy.cug.edu.cn/yangjianghai/zh_CN/index.htm', 'http://grzy.cug.edu.cn/yuqianqian/zh_CN/index.htm', 'http://grzy.cug.edu.cn/zhuzongmin/zh_CN/index.htm', 'http://grzy.cug.edu.cn/taomh/zh_CN/index.htm', 'http://grzy.cug.edu.cn/zhaoshanrong/zh_CN/index.htm']
        self.store = store

    # 获取页面信息
    def get_html(self, url):
        html = self.session.get(url)
        if html.status_code == 200:
            html.encoding = 'utf8'
            return html.text
        else:
            print(html.status_code)

    # 解析并存入excel
    def parse(self, html, url):
        try:
            soup = BeautifulSoup(html, 'lxml')
            name = soup.select_one('.name h1').text.strip()
            content = soup.select('.jbqk p')
            zhiCheng = content[0].text.strip()
            time = None
            graduateSchool = None
            gender = None
            subject = None
            for c in content:
                r = c.text.strip().split('：')
                # print(r)
                if r[0] == '入职时间':
                    time = r[1]
                if r[0] == '毕业院校':
                    graduateSchool = r[1]
                if r[0] == '性别':
                    gender = r[1]
                if r[0] == '学科':
                    subject = r[1]
            # print('-'*50)
            # print(name, zhiCheng, time, graduateSchool, gender, subject)
            url_xmxx = 'http://grzy.cug.edu.cn/' + soup.select('#nav li ul li a')[1]['href']
            url_lwcg = 'http://grzy.cug.edu.cn/' + soup.select('#nav li ul li a')[4]['href']
            # print(url_xmxx)
            # print(url_lwcg)
            soup_xmxx = BeautifulSoup(self.get_html(url_xmxx), 'lxml')
            content = soup_xmxx.select('.listnews ul li a')
            xmxx = ""
            for c in content:
                xmxx += (c.text + '\n')
            # print(xmxx)
            soup_lwcg = BeautifulSoup(self.get_html(url_lwcg), 'lxml')
            content = soup_lwcg.select('.listnews ul li a')
            lwcg = ""
            for c in content:
                lwcg += ('- ' + c['title'] + '\n')
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

    # 使用多线程运行
    def run(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            [executor.submit(self.parse(self.get_html(url), url), url) for url in self.urls]
        # for url in self.urls:
        #     self.get_html(url)
        # self.Excel_book.save('data.xls')

