import requests
from uuid import uuid4
import os
import re

URL = 'https://invest.gushi.com/stock-contest/activity/downloadPage/access?sceneID=0513&preview=0&type=1&_=1594959066501'

html = requests.get(URL)

img_url = html.json()['data']

os.path.exists('images') or os.makedirs('images')

imgs_url = [img_url['bgPicDown'], img_url['bgPicMiddle1'], img_url['bgPicMiddle2'], img_url['bgPicMiddle3'], img_url['bgPicTop'], img_url['pcChangeEffect'], img_url['pcDown'], img_url['pcQrCode']]

r_url = re.compile('http://realsscf.oss-cn-hangzhou.aliyuncs.com/FileManage/(.*)', re.I|re.S)

for i in imgs_url:
	html = requests.get(i)
	filename = r_url.findall(i)[0]
	print(filename)
	with open('images/' + filename, 'wb')as f:
		f.write(html.content)