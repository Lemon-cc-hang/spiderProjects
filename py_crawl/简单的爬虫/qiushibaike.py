import requests
from bs4 import BeautifulSoup

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.83 Safari/537.36'}
for page in range(1,2):
    html = requests.get('https://www.qiushibaike.com/text/page/{}/'.format(page), headers=headers)

    soup = BeautifulSoup(html.text, 'lxml')
    jokes = soup.select('.article')
    filename = 'qiushibaike_{}.txt'.format(page)
    with open(filename, 'wb')as f:

        for joke in jokes:
            text = joke.select('.content')[0].text.strip()
            auther = joke.select('.author h2')[0].text.strip()
            vote = joke.select('.stats-vote .number')[0].text
            comments = joke.select('.stats-comments .number')[0].text
            print('text:{}\nauther:{}\nvote:{}\ncomments:{}\n\n'.format(text,auther,vote,comments))

            f.write('text:{}\nauther:{}\nvote:{}\ncomments:{}\n\n'.format(text,auther,vote,comments).encode('utf-8'))