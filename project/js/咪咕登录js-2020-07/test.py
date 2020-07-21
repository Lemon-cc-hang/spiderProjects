import execjs

def getPwd(data):
	with open('js/pwdAndUsername.js', 'r', encoding='utf8')as f:
		content = f.read()
	jsData = execjs.compile(content)
	pwd = jsData.call('getPwd', data)
	fingerPrint = jsData.call('rsaFingerprint')['result']
	fingerPrintDetail = jsData.call('rsaFingerprint')['details']
	return pwd, fingerPrint, fingerPrintDetail


mm = getPwd('123456')
pwd = mm[0]
fingerPrint = mm[1]
fingerPrintDetail = mm[2]
username = getPwd('11111111111')[0]
print('username: ' + username)
print('pwd: ' + pwd)
print('fingerPrint: ' + fingerPrint)
print('fingerPrintDetail: ' + fingerPrintDetail)