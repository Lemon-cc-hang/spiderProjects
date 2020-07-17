import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


class ThreeSpider:
    def __init__(self, store):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
                   'Referer': 'http://grzy.cug.edu.cn/jsjx.jsp?urltype=tree.TreeTempUrl&wbtreeid=1016'}

        self.session = requests.session()
        self.session.headers = headers
        self.urls = ['http://grzy.cug.edu.cn/KaiCao/zh_CN/index.htm', 'http://grzy.cug.edu.cn/DavidKemp/zh_CN/index.htm', 'http://grzy.cug.edu.cn/lihui/zh_CN/index.htm', 'http://grzy.cug.edu.cn/denghao/zh_CN/index.htm', 'http://grzy.cug.edu.cn/liyilong/zh_CN/index.htm', 'http://grzy.cug.edu.cn/shentianyi/zh_CN/index.htm', 'http://grzy.cug.edu.cn/shimin/zh_CN/index.htm', 'http://grzy.cug.edu.cn/mayiming/zh_CN/index.htm', 'http://grzy.cug.edu.cn/wangan/zh_CN/index.htm', 'http://grzy.cug.edu.cn/wangjunpeng/zh_CN/index.htm', 'http://grzy.cug.edu.cn/wangxinshui/zh_CN/index.htm', 'http://grzy.cug.edu.cn/Yanjiaxin/zh_CN/index.htm', 'http://grzy.cug.edu.cn/wanghuapei/zh_CN/index.htm', 'http://grzy.cug.edu.cn/xuezhenhua/zh_CN/index.htm', 'http://grzy.cug.edu.cn/XianbingXu/zh_CN/index.htm', 'http://grzy.cug.edu.cn/zhanghao/zh_CN/index.htm', 'http://grzy.cug.edu.cn/liupenglei/zh_CN/index.htm', 'http://grzy.cug.edu.cn/XiongQing/zh_CN/index.htm', 'http://grzy.cug.edu.cn/zhaodeai/zh_CN/index.htm', 'http://grzy.cug.edu.cn/huangjun/zh_CN/index.htm']
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
            name = soup.select_one('.t_photo span').text.strip()
            zhiCheng = soup.select('.p_left .p_l_nr .t_jbxx_nr p')[0].text.strip()
            content = soup.select('.p_left .p_l_nr .t_jbxx_nr p')
            time = None
            graduateSchool = None
            gender = None
            subject = None
            for c in content:
                r = c.text.strip().split(':')
                # print(r)
                if r[0].strip() == '入职时间':
                    time = r[1]
                if r[0].strip() == '毕业院校':
                    graduateSchool = r[1]
                if r[0].strip() == '性别':
                    gender = r[1]
                if r[0].strip() == '学科':
                    subject = r[1]
            # print('-'*50)
            # print(time, graduateSchool, gender, subject)
            # print(zhiCheng)
            url_xmxx = 'http://grzy.cug.edu.cn/' + soup.select('#nav .nLi .sub li a')[1]['href']
            url_lwcg = 'http://grzy.cug.edu.cn/' + soup.select('#nav .nLi .sub li a')[4]['href']
            # print(url_xmxx)
            # print(url_lwcg)
            soup_xmxx = BeautifulSoup(self.get_html(url_xmxx), 'lxml')
            content = soup_xmxx.select('.t_list_nr li a')
            xmxx = ""
            for c in content:
                xmxx += ('- ' + c.text.strip() + '\n')
            # print(xmxx)
            soup_lwcg = BeautifulSoup(self.get_html(url_lwcg), 'lxml')
            content = soup_lwcg.select('.t_list_nr li a')
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


    def run(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            [executor.submit(self.parse(self.get_html(url), url), url) for url in self.urls]
        # self.Excel_book.save('data.xls')
