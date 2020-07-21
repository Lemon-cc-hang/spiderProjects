import requests
from pprint import pprint
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
import os
from uuid import uuid4


class Spider:
	def __init__(self, kw):
		headers = {'Cookie': 'BIDUPSID=0F981BD8BBFE86641C34EBEC41E106E1; PSTM=1593096352; BAIDUID=0F981BD8BBFE86646130C8489993E86D:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=X5ZYU1iT2Q3MHZqOUVyYTl-TVRGdjRDZGxXN21mc1V4WFZVczdoSUZUUFNReUpmSVFBQUFBJCQAAAAAAAAAAAEAAAClKY1UtPK9tNPNZGXUxgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANK2-l7StvpeZ; delPer=0; PSINO=7; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=31909_1449_31325_32139_31253_32045_32231_31709_32108_26350_31639_22159; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; userFrom=www.baidu.com',
		           'Referer': 'https://www.baidu.com/s?wd=python&rsv_spt=1&rsv_iqid=0xe3cdc51c0000e884&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_sug3=19&rsv_sug1=14&rsv_sug7=100&rsv_sug2=0&rsv_btype=i&inputT=6106&rsv_sug4=7225',
		           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
		self.session = requests.session()
		self.session.headers = headers
		if kw == '':
			kw = '美女'
			self.kw = quote(kw)
		else:
			self.kw = quote(kw)
		self.filename = './images/{}'.format(kw)
		if not os.path.exists(self.filename):
			os.makedirs(self.filename)

	def __get_url(self, url):
		html = self.session.get(url)
		if html.status_code == 200:
			try:
				for data in html.json()['data'][:-1]:
					try:
						image_url = data['middleURL']
						self.__download_img(image_url)
					except Exception as e:
						pass
			except Exception as e:
				pass
		else:
			print('[ERROR] ', html.status_code)

	def __download_img(self, image_url):
		img = self.session.get(image_url)
		print('[INFO] 正在储存 >>> ', image_url)
		with open(self.filename + '/{}.jpg'.format(uuid4()), 'wb')as f:
			for chunk in img.iter_content(1024):
				f.write(chunk)

	def run(self):
		urls = [
			'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&queryWord={}&word={}&pn={}&rn=30'.format(
				self.kw, self.kw, i) for i in range(60, 2000, 30)]
		with ThreadPoolExecutor(max_workers=20)as t:
			for url in urls:
				t.submit(self.__get_url, url)


if __name__ == '__main__':
	spider = Spider(input('请输入需要查找的关键词 >>> '))
	spider.run()