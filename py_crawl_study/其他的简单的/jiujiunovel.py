import requests
from bs4 import BeautifulSoup


def AutoDownload():
    list_url = []
    list2_url = []
    download = []
    titles = []
    titles2 = []
    page = 37

    # https://www.jjxsw.la/e/action/ListInfo.php?page=1&classid=37&line=10&tempid=3&ph=1&andor=and&orderby=2&myorder=0
    # https://www.jjxsw.la/e/DownSys/doaction.php?enews=DownSoft&classid=37&id=22518&pathid=1&pass=ee247a67a5adcf1dfb1abecbd1ff5635&p=:::
    def requests_html(url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.83 Safari/537.36'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            return None

    def first_scraper(url):
        """
        获取第一个网页信息
        :param url: 获取第一个网页中页面的地址
        :param headers: 伪装头
        :return: None
        """
        html = requests_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        bodys = soup.select('.listbg')
        for body in bodys:
            title = body.select('a')[0]['title']
            titles.append(title)
            down_load = body.select('.img')[0]['href']
            print('已经获取第一个地址https://www.jjxsw.la{}'.format(down_load))
            list_url.append('https://www.jjxsw.la' + down_load)

    def second_scraper(url):
        """
        获取第二个网页信息
        :param url: 获取第二个网页中的下载地址网页
        :param headers: 伪装头
        :return: None
        """
        html = requests_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        down_load = soup.select('.downAddress_li a')[0]['href']
        print('已经获取第二个地址https://www.jjxsw.la{}'.format(down_load))
        list2_url.append('https://www.jjxsw.la' + down_load)

    def download_url(url):
        """
        下载url获取
        :param url:这个网页的url
        :param headers: 伪装头
        :return: None
        """
        html = requests_html(url)
        soup = BeautifulSoup(html, 'html.parser')
        down_load = soup.select('#Frame .strong.green')[1]['href']
        print('已经获取下载地址https://www.jjxsw.la{}'.format(down_load))
        download.append('https://www.jjxsw.la' + down_load)

    for i in range(1, page + 1):
        # URL = 'https://www.jjxsw.la/e/action/ListInfo.php?page={}&classid=37&line=10&tempid=3&ph=1&andor=and&orderby=2&myorder=0'.format(i)
        URL = 'https://www.jjxsw.la/txt/Kongbu/index_{}.html'.format(i)
        first_scraper(URL)

        for j in list_url:
            second_scraper(j)

        for j in list2_url:
            download_url(j)

        print('titles:{}\ndownload:{}\n\n'.format(titles, download))

        for j in range(len(download)):
            filename = titles[j] + '.rar'
            resource = requests.get(download[j], stream=True)

            with open(filename, 'wb')as f:
                for chunk in resource.iter_content(1024):
                    f.write(chunk)
                print(titles[j] + '已下载完成')
        titles2 += titles
        list_url = []
        list2_url = []
        download = []
        titles = []

    with open('list.txt', 'w')as f:
        for i in titles2:
            f.write(i + '\n')


if __name__ == '__main__':
    AutoDownload()
