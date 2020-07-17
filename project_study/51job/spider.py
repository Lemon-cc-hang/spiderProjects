# https://search.51job.com/list/130000%252C020000%252C010000%252C030200%252C040000,000000,0000,00,9,99,%25E7%2588%25AC%25E8%2599%25AB,2,1.html
# https://search.51job.com/list/130000%252C020000%252C010000%252C030200%252C040000,000000,0000,00,9,99,%25E7%2588%25AC%25E8%2599%25AB,2,2.html
# https://search.51job.com/list/130000%252C020000%252C010000%252C030200%252C040000,000000,0000,00,9,99,%25E7%2588%25AC%25E8%2599%25AB,2,1.html
import requests
from bs4 import BeautifulSoup
import csv


class Spider:
    def __init__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
            'Cookie': 'partner=www_google_com_hk; guid=c683f7d43607135c25590aafad95853a; 51job=cenglish%3D0%26%7C%26; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60130000%2C020000%2C010000%2C030200%2C040000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60130000%2C020000%2C010000%2C030200%2C040000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%C5%C0%B3%E6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60130800%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%C5%C0%B3%E6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60130800%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%C5%C0%B3%E6%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21'}
        self._session = requests.session()
        self._session.headers = headers
        self._urls = [
            'https://search.51job.com/list/020000%252C010000%252C030200%252C040000%252C180200,000000,0000,00,9,99,%25E7%2594%25B5%25E5%25AD%2590%25E5%2595%2586%25E5%258A%25A1,2,{}.html'.format(
                i) for i in range(1, 4)]
        self._new_url = []
        row = ('title', 'company', 'info')

        with open('data.csv', 'w', encoding='gbk')as f:
            f_writer = csv.writer(f)
            f_writer.writerow(row)

    def __get_html(self, url):
        html = self._session.get(url)
        if html.status_code == 200:
            html.encoding = 'gbk'
            return html.text
        else:
            print(html.status_code)

    def __get_url(self, url):
        soup = BeautifulSoup(self.__get_html(url), 'lxml')
        body = soup.select('#resultList > .el')
        for b in body[1:]:
            url = b.select_one('.t1 span a')['href']
            self._new_url.append(url)

    def __parse(self, url):
        try:
            soup = BeautifulSoup(self.__get_html(url), 'lxml')
            body = soup.select(
                "body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_main > div:nth-child(1) > div > p")
            title = soup.select_one(
                'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > h1').text.strip().replace(
                u'\xa0', u'')
            company = soup.select_one(
                'body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > p.cname > a.catn').text.strip().replace(
                u'\xa0', u'')
            info = ""
            for b in body:
                info += b.text.strip().replace(u'\xa0', u'')
                # row = [title, company, info]
            # print(info)
            if info == "":
                info = None
            row = (title, company, info)
            self.__csv_write(row)
        except Exception as e:
            print(e)

    def __csv_write(self, row):
        with open('data.csv', 'a+', encoding='gbk')as f:
            f_writer = csv.writer(f)
            f_writer.writerow(row)

    def run(self):
        print("[INFO]正在获取url．．．")
        for url in self._urls:
            self.__get_url(url)
        print('[INFO]正在存储数据．．．')
        for url in self._new_url:
            self.__parse(url)
        print("[SUCCESS]存储数据成功．．．")
