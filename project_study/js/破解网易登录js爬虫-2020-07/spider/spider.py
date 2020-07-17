import requests
import re
import execjs
import time


class NE(object):
	def __init__(self, username, password):
		self.username = username
		self.password = password
		headers = {'Cookie': 'hb_MA-B154-F82F55E16A53_source=www.google.com.hk; _ihtxzdilxldP8_=30; JSESSIONID-WYTXZ=WuoNGsYFm5D%5CrczL63VOiNJb7klbrDOOI%2BSS7JqTDU5yNYtnXaAFvdcHNYb0UQyl7eUUj70Ja9xSGsSvzPKc9Kjf53x3M4GdT%5CTegnp3upeDpWMUautCGz5w%2BIx9%2BbVM4MoVCNpeZJpFtdaFMrV2wngzXr0ctFOdClUbqKNzTqd6yUz7%3A1593168094208; _mloixed92=30; l_yd_s_studytajyMJn=91DEFABDECBEF89EBD693D877098C838F9C40F095EE7E389706AE771CD8E326FD0DC7A7E5B58BF4B7939A8B355F47433C964C0DC1EDF9750603C21A6DDB814BAD804AA11FB74FA8472C2B903EA38C5C849316CF95C012F2C5A90831C56BF22553B679756B2B6675AF453618219D2020B; l_s_studytajyMJn=91DEFABDECBEF89EBD693D877098C838F9C40F095EE7E389706AE771CD8E326FD0DC7A7E5B58BF4B7939A8B355F47433539B8F3311463E0B7DF2B3A9C01D6D9447E2D9047C0E556ADF32CBDA70D2B41B31E4682B8C0D3B6E99A1E718396AE79EF3A45FE2C785CA12825006A8035BF309; ntes_zc_cid=b0532b0d-e632-43af-993c-87b6a100145d; ntes_zc_yd_tajyMJn=91DEFABDECBEF89EBD693D877098C838F9C40F095EE7E389706AE771CD8E326F8A724208E0FB4945B8754CAA3FA60A15D93823649C6ACBBB81A026ECF4EFC2FC7CE7EE75E805701D18A9BF116F039D6D; _9755xjdesxxd_=32; YD00000710348764%3AWM_NI=0GOfBX3hlsNnUkE4KiIMtFOmrGYQeP50uQPWw7cgwcERY7mjrivTiegbwQzeUMybAin4WVJNbf%2BGlxFG1j14THcDlGfBXV8qWR%2Bw5gckO5Uae97F7J1kURua8krpfigBVlY%3D; YD00000710348764%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb1f63996e8b9d2b65a88eb8aa2d14e828f8aaff55da6b18bb2c54793acb890f32af0fea7c3b92af4998187c154f1b8a494cd6697b58bd5ca638b93bca7ce67b29997b2e85cf7f0bbb2d35db5e9ad88f669878e97d8f062b2b7bab5ec6fa5beb9b2f96f9793b783c463aeec99b7c946a2bae5a8ef748699ff8bb4409898ada5ef4da69e98b7bb7b958ee598b86da1b581d6d86ba7e7f9a7b642f3b59bb3f86bfcb5be91e563a59e9a8ddc37e2a3; YD00000710348764%3AWM_TID=CpYvR%2BT%2F2EhFUFBFERc6WPsRRQMU9h85; l_yd_sign=-020170531z0fAbMba64zO9_5tzMjpymjomSzuk9BtCYlE0OPZXxo9Cooe2l6ZDfE_E0lHaDuN5oK5_CVoIGr07JIwU_gelwO7ofTNZ8omc6Scmd63VVGw..; THE_LAST_LOGIN_MOBILE=17679377069; _ntes_nuid=0da853736ff406ad91f3127ea0c28c16; NTES_hp_textlink1=old; _ntes_nnid=526e0f2f188162f992d16e2dbc8fa428,1593186682631; P_INFO=17679377069|1593164520|2|study|00&99|null&null&null#jix&360700#10#0#0|&0||17679377069; utid=kKvlHsJCjLIjhPNI5FbNdLvXlA5bH2Qy; l_s_163MODXOXd=5B4AE6BFF238CE247A553C01A50AC39045513F95F87E19FA0AC69B2F6E3811383691AECB359EF46C0BD6F87DCCD77C107E9B58201E5C50DB201DF22EB5B998834E29188CD4759F2A17772F77FFF6F6B7501BBE27209EB209A5BAE1D06408F9D1; gdxidpyhxdE=0GQw753z4pAWv0C%2Fn4IT47IvCCdqujf%2FvMUZqSRJdpjGx%2BgoYWl9X4aSia2ZOb%5CtBdQkMmbZDynK19U04r2Mq10K52jhIpDI%5Czn%2FNI%2BejuAc660zwi7J5QxiruU2qNJXWpYirE7lVoQY8GMqRBJY7MmRAxUMdqGYlG%5CYBRbxcKaKwCEv%3A1593225074902; JSESSIONID-WYTXZDL=kFSS%5CiXKumKj%5C3wz%2FjIQyI6YOXjboRdL6ZA06D8ARz68XXnLkvOi2rIiuJ0JoEHy%2BHujaj9%2Fgu10u%2FYhrnqS6%2BGpheqdRk8%5Ccvfps1wVucnKMrFzxXhh0dmpI6F2Od4RPdhGwe0qBO3QiKLdu2ktrkQVdAhxviRR7mNOw%2F1X7FsaeGuX%3A1593225014984',
		           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
		self.session = requests.session()
		self.session.headers = headers

	def __getPassword(self):
		with open('../js/netease.js', 'r', encoding='utf8')as f:
			content = f.read()
		jsData = execjs.compile(content)
		self.pw = jsData.call('getPw', self.password)
		print('pw:', self.pw)

	def __getRTid(self):
		with open('../js/rtid.js', 'r', encoding='utf8')as f:
			content = f.read()
		jsData = execjs.compile(content)
		self.rTid = jsData.call('getRTid')
		print('rTid:', self.rTid)

	def __getTk(self):
		url = 'https://dl.reg.163.com/dl/gt'
		params = {
			'un': self.username,
			'pkid': 'MODXOXd',
			'pd': '163',
			'topURL': 'https://www.163.com/',
			'rtid': self.rTid,
			'nocache': time.time()*1000
		}
		html = self.session.get(url, params=params)
		self.tk = html.json()['tk']
		print(self.tk)

	def __login(self):
		url = 'https://dl.reg.163.com/dl/l'
		data = {
			'channel': '0',
			'd': '10',
			'domains': "163.com",
			'l': '0',
			'pd': '163',
			'pkid': 'MODXOXd',
			'pw': self.pw,
			'pwdKeyUp': '1',
			'rtid': self.rTid,
			't': time.time()*1000,
			'tk': self.tk,
			'topURL': 'https://www.163.com/',
			'un': self.username
		}
		html = self.session.post(url, json=data)
		print(html.json())

	def run(self):
		self.__getPassword()
		self.__getRTid()
		self.__getTk()
		self.__login()


if __name__ == '__main__':
	spider = NE('a1029516811@163.com', 'diaoHANG3')
	spider.run()