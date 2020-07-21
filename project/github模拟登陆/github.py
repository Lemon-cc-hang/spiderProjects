import requests
import time
from bs4 import BeautifulSoup

headers = {
	'Cookie': '_octo=GH1.1.721453151.1586831679; _ga=GA1.2.561782820.1586831682; '
	          'experiment:homepage_signup_flow'
	          '=eyJ2ZXJzaW9uIjoiMSIsInJvbGxPdXRQbGFjZW1lbnQiOjY0LjY0NTM0Njk0NDM3MDYyLCJzdWJncm91cCI6bnVsbCwiY3JlYXRlZEF0IjoiMjAyMC0wNC0xNlQxNDozOToxNi4zNDFaIiwidXBkYXRlZEF0IjoiMjAyMC0wNC0yNlQwNDoyMzoyNi45MTJaIn0=; _device_id=e79698717e686a000c70e697570d05fb; _gid=GA1.2.2033272965.1589446509; tz=Asia%2FShanghai; has_recent_activity=1; _gat=1; logged_in=no; _gh_sess=bcqy9XmShX9qHCeaZEBWjhb1xGT61HjI%2FdS1FhylrBfCPgXwnPmivuOZ2lbkwNtCxX9M9Db%2BoYD6zjHvxefXFj8ZFJE7ChA2Owahhydok2Nz3mv2JRtHUld5J9YDEpzuAqTMfx2mLN%2FCKXxqwP%2FqQEXMJN8dO386kmccilUHqhONgieTDG%2Fc%2Bh3OIy%2FdK2iU%2BCnaDg1cogD%2FcWxpVKkqyoxmPllSLM0u%2B1ZF2FjT0%2FeqacnF1txZZ4ug%2FSxBIPAhh51Pdvda535jrsN2hBa8KQ%3D%3D--429PRhApYRoBD1k%2F--745C7ulI9R4VPlUhlZLrKA%3D%3D',
	'Referer': 'https://github.com/login',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
	              'like Gecko) Chrome/81.0.4044.83 Safari/537.36'}

session = requests.session()
session.headers = headers


def save_html(html):
	with open('login.html', 'w', encoding='utf8')as f:
		f.write(html)


def post_github(url):
	data = {'commit': 'Sign in',
	        'authenticity_token':
		        'sj5fa1Cqr9JuurCfiJxCmmJLyD9rpv7iTK1bpVCVJ6GdcOltKQ8P999XOdy1jpN1mILSMKCRN4NKUzmm'
		        '+FGqOw==',
	        'login': '',
	        'password': '',
	        'webauthn-support': 'supported',
	        'webauthn-iuvpaa-support': 'supported',
	        'timestamp': '{}'.format(time.time()),
	        'timestamp_secret': 'd5bb34e685fd14b8dc14decbc444f8f7db5bba950c67eeaa4a46307e606c524e'}
	html = session.post(url, headers=headers, data=data)
	if html.status_code == 200:
		print('正在存储html')
		save_html(html.text)
		get_feed(session)

	else:
		print(html.status_code)


def get_feed(sess):
	html = sess.get('https://github.com/dashboard-feed')
	if html.status_code == 200:
		print("正在解析页面．．．")
		parse_html(html.text)


count = 0


def parse_html(html):
	soup = BeautifulSoup(html, 'html.parser')
	datas = soup.select('div.watch_started')
	for data in datas:
		global count
		try:
			from_people = data.select('.d-flex.flex-items-baseline div a')[0].text
			to_people = data.select('.d-flex.flex-items-baseline div a')[1].text
			code = ''
			if to_people:
				code = soup.select('span.ml-0')[count].text.replace('\n', '').replace('\t', '')
				count += 1
			# print(to_people)
			save_data("from:{} to:{} code:{}".format(from_people, to_people, code))
		# print("from:{} to:{} code:{}".format(from_people, to_people, code))

		except:
			pass


def save_data(row):
	with open('github_data.txt', 'a+', encoding='utf8')as f:
		f.write(row + '\n')


if __name__ == '__main__':
	url = 'https://github.com/session'
	post_github(url)