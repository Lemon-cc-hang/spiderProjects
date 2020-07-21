# https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=20&type=T
# https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=40&type=T
import aiohttp
from bs4 import BeautifulSoup
from douban_db import sess, Book
import asyncio

headers = {
    'Cookie': 'bid=g8lce5eQwrQ; ll="118215"; _vwo_uuid_v2=D10BCEA3BCDE6A01A8D59A1A7875B5D3B|384b00ca04ab15c08791dc9e5a7295cf; __utma=30149280.695660836.1586790657.1589459555.1589533244.5; __utmz=30149280.1589533244.5.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=30149280; __utmt=1; ap_v=0,6.0; gr_user_id=3f63eb57-4c08-4d6a-8cef-7f43c5baf969; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=c4b7cd18-ffd1-46d6-8dd8-f90411af6ac3; gr_cs1_c4b7cd18-ffd1-46d6-8dd8-f90411af6ac3=user_id%3A0; __utmt_douban=1; __utma=81379588.852483606.1589533246.1589533246.1589533246.1; __utmc=81379588; __utmz=81379588.1589533246.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1589533246%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_c4b7cd18-ffd1-46d6-8dd8-f90411af6ac3=true; _pk_id.100001.3ac3=073d8f0e5d779134.1589533246.1.1589533266.1589533246.; __utmb=30149280.5.10.1589533244; __utmb=81379588.4.10.1589533246',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.83 Safari/537.36'}


async def get_html(i):
    url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={}&type=T'.format(i)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url)as resp:
            if resp.status == 200:
                print('parsing ...')
                html = await resp.text()
                await parse_html(html)

            else:
                print('ERROR')


async def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    books = soup.select('li.subject-item')
    for book in books:
        try:
            title = book.select_one('.info h2 a').text.strip().replace(' ', '').replace('\n', '')
            tag = book.select_one('.info .pub').text.strip().replace(' ', '').replace('\n', '')
            star = book.select_one('.info .rating_nums').text
            pl = book.select_one('.info .pl').text.strip()
            introduce = book.select_one('.info p').text.strip()

            # 插入数据库

            book_data = Book(
                title=title,
                info=tag,
                star=star,
                pl=pl,
                introduce=introduce
            )
            sess.add(book_data)
            sess.commit()
        except Exception as e:
            print(e)
            sess.rollback()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [get_html(i) for i in range(20, 1000, 20)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()