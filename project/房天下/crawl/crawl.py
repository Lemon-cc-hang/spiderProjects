import requests
from lxml import etree
import re
from urllib import parse
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from fangtianxia_db import sess, House


class Crawl:
    def __init__(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'cookie': 'city=sh; global_cookie=4qrrf1mbprggiwxulshblmpik1vkbqex27m; integratecover=1; __utma=147393320.1577720239.1592825119.1592825119.1592825119.1; __utmc=147393320; __utmz=147393320.1592825119.1.1.utmcsr=sh.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ASP.NET_SessionId=oul4nkwpiwvyjmuoihcirgt2; Rent_StatLog=998ff119-091e-4a47-b217-c29049f256ec; g_sourcepage=zf_fy%5Elb_pc; Captcha=5065733176634C75377061622B746E5A6C7654374238597239706475786A68566931314E31465449544B4F45534831715466486F4E69634B3653745633596C3543732B2B4C30795A324F6B3D; unique_cookie=U_4qrrf1mbprggiwxulshblmpik1vkbqex27m*10',
            'referer': 'https://sh.fang.com/'}

        self.session = requests.session()
        self.session.headers = headers
        self.urls = ['https://zu.fang.com/house-a0{}/'.format(i) for i in range(1, 17)] + [
            'https://sh.zu.fang.com/house-a0{}/'.format(i) for i in range(18, 36)]

    # 正则表达式匹配数字
    def __get_number(self, text):
        number = re.compile('\d+')
        return number.findall(text)[0]

    # 获取第一页的页面
    def __get_index(self, url):
        print('[INFO] 正在获取 index 文本．．．')
        html = self.session.get(url)
        if html.status_code == 200:
            self.__get_data(html.text, url)
        else:
            print(html.status_code)

    # xpath定位页面让正则匹配
    def __get_pages(self, html):
        try:
            soup = etree.HTML(html)
            pages = soup.xpath('//div/*[@class="fanye"]/span/text()')[0]
            number = self.__get_number(pages)
            if number:
                return int(number)
            return None
        except Exception as e:
            print(e)

    # 获取页面文本, 返回文本
    def __get_html(self, url):
        html = self.session.get(url)
        if html.status_code == 200:
            return html.text
        else:
            print('[ERROR]', html.status_code)

    # 解析第一页的文本
    def __get_data(self, html, url):
        pages = self.__get_pages(html)
        if not pages:
            pages = 0
        urls = [url + 'i3{}/'.format(i) for i in range(1, pages+1)]
        with ThreadPoolExecutor(max_workers=100)as t:
            for url in urls:
                t.submit(self.__get_data_next(self.__get_html(url)))

    # 获取房子的数据
    def __get_house_data(self, href, *args):
        print('[INFO] 正在获取房子数据．．．')
        html = self.__get_html(href)
        # print(html)
        r = re.compile('<a class="btn-redir" style="font-size: 14pt;" href="(.*?)">点击跳转</a>', re.I | re.S)
        url = r.findall(html)[0]
        html = self.__get_html(url)
        # print(html)
        soup = etree.HTML(html)
        lines = soup.xpath('//div[@class="fyms_con floatl gray3"]')
        results = ""
        for line in lines:
            data = line.xpath('text()')[0]
            results += ('|' + data)

        # print(args, results)
        s = sess()
        try:
            # print(s)
            house = House(
                title=args[0],
                block=args[1],
                rent=args[2],
                data=results
            )
            s.add(house)
            s.commit()
            print("[SUCCESS]Commit．．．")
        except Exception as e:
            print("[ERROR]RollBack．．．", e)
            s.rollback()

    # 获取房子数据的url
    def __get_data_next(self, html):
        soup = etree.HTML(html)
        dls = soup.xpath('//dl[@class="list hiddenMap rel"]')
        for dl in dls:
            try:
                title = dl.xpath('dd/p[@class="title"]/a/text()')[0]
                rent = dl.xpath('dd/div/p[@class]/span/text()')[0]
                block = dl.xpath('//dl[@class="list hiddenMap rel"]/dd/p[@class="gray6 mt12"]/text()')[0]
                href = parse.urljoin('https://zu.fang.com/', dl.xpath('dd/p[@class="title"]/a/@href')[0])
                # print(title, rent, href)
                self.__get_house_data(href, title, block, rent)

            except IndexError as e:
                print('dl error', e)

    # 运行函数
    def run(self):
        with ProcessPoolExecutor(max_workers=20)as p:
            for url in self.urls:
                p.submit(self.__get_index(url))

        self.session.close()


if __name__ == '__main__':
    crawl = Crawl()
    crawl.run()
