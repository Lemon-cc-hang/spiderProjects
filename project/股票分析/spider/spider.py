"""
爬取股票数据
"""
import time
import csv
import requests
from fangtianxia_db import sess, StockData

url = 'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SH510050&begin=1593486392812&period=day&type=before&count=-142&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'

class Spider:
	# 初始化代码
	def __init__(self):
		headers = {'Cookie': 'xq_a_token=ea139be840cf88ff8c30e6943cf26aba8ad77358; xqat=ea139be840cf88ff8c30e6943cf26aba8ad77358; xq_r_token=863970f9d67d944596be27965d13c6929b5264fe; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5NDAwMjgwOCwiY3RtIjoxNTkzMzk4NzI3OTQ5LCJjaWQiOiJkOWQwbjRBWnVwIn0.iB26VJhQxtm-vgutQVm9GX3Cg_sQSeFy-TgU0mxa4gHVQRq0dWyNT6JuL9fdyObm6-nDVBiffAW4fSz1Pj_i8pF_PWMgpZ4gxKFBtuzIquRawfuDmtCOFJpVIxfntG96HlEBDdvmOLCa4YFEzDq1f8-Cix1xyNz79YAgH0kloXPL6FROrDwnose0mkn2I_scNSrAPPtad9pVQLpjoFwtF7KtelcSJZRYfn4YO_r93tgrxY--C8uFrikLt-zOqWrUQuh41qHXEIDlR_xNfnD6i_c1yik6-4xrKxHSpRDkb8RuApngxg7-kbQNOAdluptZ1TqOtLMhVQKzcfM7pK9R5w; u=551593398741657; device_id=1958aac73b104fb7fea591c487a44722; is_overseas=0; Hm_lvt_1db88642e346389874251b5a1eded6e3=1593398743,1593399822,1593399991; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1593399991',
		           'Origin': 'https://xueqiu.com',
		           'Referer': 'https://xueqiu.com/S/SH510050',
		           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
		self.session = requests.session()
		self.session.headers = headers

	# 将毫秒数 转换为 日期
	def __convertTimeText(self, time1):
		timeStamp = int(time1)
		timeStamp /= 1000.0
		print(timeStamp)
		timeArr = time.localtime(timeStamp)
		otherStyleTime = time.strftime("%Y-%m-%d", timeArr)
		return otherStyleTime

	# 获取json接口数据
	def __get_json(self, c):
		with open('../data/data_{}.csv'.format(c), 'w', encoding='utf8')as f:
			row = ('date', 'open', 'high', 'low', 'close')
			f_write = csv.writer(f)
			f_write.writerow(row)
		html = self.session.get(self.url)
		if html.status_code == 200:
			print('time', 'open', 'high', 'low', 'close')
			for item in html.json()['data']['item']:
				date = self.__convertTimeText(item[0])
				open1 = item[2]
				high = item[3]
				low = item[4]
				close1 = item[5]
				print(date, open1, high, low, close1)
				self.__store2Csv(date, open1, high, low, close1, c)
				self.__store2DB(date, open1, high, low, close1, c)
		else:
			print("[ERROR] 返回的状态码为" + str(html.status_code))

	# 储存为csv 格式, 用于可视化分析
	def __store2Csv(self, *args):
		with open('../data/data_{}.csv'.format(args[-1]), 'a+', encoding='utf8')as f:
			row = (args[0], args[1], args[2], args[3], args[4])
			f_write = csv.writer(f)
			f_write.writerow(row)

	# 储存数据库
	def __store2DB(self, *args):
		s = sess()
		try:
			stock = StockData(
				name=args[-1],
				date=args[0],
				open=args[1],
				high=args[2],
				low=args[3],
				close=args[4]
			)
			s.add(stock)
			s.commit()
			print('[SUCCESS] Commit．．．')
		except Exception as e:
			s.rollback()
			print('[ERROR] RollBack．．．', e)

	# 运行函数
	def run(self):
		comp = ['SH510310', 'SH510050', 'SZ159915']
		for c in comp:
			self.url = "https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={}&begin=1593486392812&period=day&type=before&count=-142&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance".format(c)
			self.__get_json(c)


# 运行
if __name__ == '__main__':
	spider = Spider()
	spider.run()