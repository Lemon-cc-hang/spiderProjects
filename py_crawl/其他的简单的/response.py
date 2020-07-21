import requests
from bs4 import BeautifulSoup

URL = 'http://query.sse.com.cn/security/stock/queryCompanyBulletin.do?jsonCallBack=jsonpCallback77374&isPagination=true&productId=&securityType=0101%2C120100%2C020100%2C020200%2C120200&reportType2=DQBG&reportType=&beginDate=2019-07-01&endDate=2019-07-31&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1586516138825'
HEADERS = {'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/regular/'}

html = requests.get(URL, headers=HEADERS)

soup = BeautifulSoup(html.text, 'html.parser')

# untreated_data = soup[19,-1]


print(soup)

# http://static.sse.com.cn//disclosure/listedinfo/announcement/c/2019-07-31/600011_2019_z.pdf
#