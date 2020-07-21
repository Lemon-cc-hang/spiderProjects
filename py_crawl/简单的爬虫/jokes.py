import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.83 Safari/537.36'}
for i in range(1, 2):
    html = requests.get('http://xiaohua.zol.com.cn/lengxiaohua/{}.html'.format(i), headers=headers)

    soup = BeautifulSoup(html.text, 'lxml')
    jokes = soup.select('.article-summary')
    page = i
    filename = 'jokes_{}.txt'.format(page)
    with open(filename, 'w')as f:
        for joke in jokes:
            title = joke.select('.article-title')[0].text
            source = joke.select('.article-source')[0].text.replace('来源：', '').strip()
            all_url = joke.select('.all-read')[0]['href']
            print('title:\r\n{}\r\nsource:\r\n{}\r\nall_url:\r\n{}'.format(title, source, all_url))
            bodys = joke.select('.summary-text p')
            print('joke:')
            for body in bodys:
                body = body.text.strip()
                print(body, '\r\n')

            f.write('title:{}\r\nsource:{}\r\nall_url:{}\r\njoke:{}\r\n'.format(title, source, all_url, bodys))
