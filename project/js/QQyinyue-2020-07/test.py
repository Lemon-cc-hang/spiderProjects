import requests
from urllib.parse import quote
import execjs
import urllib
from pprint import pprint


def __getSign(data):
	with open('./sign/sign.js', 'r', encoding='utf8')as f:
		content = f.read()
	jsData = execjs.compile(content)
	sign = jsData.call('getSign', data)
	return sign

mid = '001glaI72k8BQX'
headers = {'cookie': 'pgv_pvi=1658514432; RK=qQwsm86yR1; ptcz=c2555f5a08ebb09541d645152b8eb7f0731d77a0ae3d0a20b5fee398760a3ea2; pgv_pvid=3449912178; skey=@teC22CK1J; pgv_si=s2309940224; pgv_info=ssid=s785782265; ts_refer=www.google.com.hk/; ts_uid=7747570870; userAction=1; yqq_stat=0; player_exist=1; qqmusic_fromtag=66; psrf_qqrefresh_token=41BA7069ECE263DB3D879F401C02F9C8; psrf_musickey_createtime=1593236318; qqmusic_key=Q_H_L_2urssx50eWDGVC5uP_D_ysxCKkG-LFQ3ZkkCMQKWzgpzsukuONpAz9RGDd06jj8; tmeLoginType=2; uin=4831703; psrf_qqopenid=331F40A04A05EC1494E427EA7E406767; euin=7ecioKSzoz**; qm_keyst=Q_H_L_2urssx50eWDGVC5uP_D_ysxCKkG-LFQ3ZkkCMQKWzgpzsukuONpAz9RGDd06jj8; psrf_qqaccess_token=4F09ED9998363682A8AF40DD0CCDD504; psrf_qqunionid=A6391CE6D325C05177B721D6C301A67A; psrf_access_token_expiresAt=1601012318; ts_last=y.qq.com/n/yqq/song/000Ka7OA0aSOGf.html; yplayer_open=1; yq_index=0',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
           'referer': 'https://y.qq.com/portal/player.html'}
data = '{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"3449912178","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"3449912178","songmid":["%s"],"songtype":[0],"uin":"4831703","loginflag":1,"platform":"20"}},"comm":{"uin":4831703,"format":"json","ct":24,"cv":0}}'% mid


url = 'https://u.y.qq.com/cgi-bin/musics.fcg?sign={}&loginUin=4831703&hostUin=0&data={}'.format(__getSign(data), quote(data))
html = requests.get(url, headers=headers)
# pprint(html.json())
_url = html.json()['req_0']['data']['midurlinfo'][0]['vkey']
# pprint(_url)
url = 'https://isure.stream.qqmusic.qq.com/C400{}.m4a?guid=3449912178&vkey={}&uin=6615&fromtag=66'.format(mid, _url)
print(url)
# https://isure.stream.qqmusic.qq.com/C400000Ka7OA0aSOGf.m4a?guid=3449912178&vkey=899B129319E51E829FC310BE9A959D0A7B749E1D1078661AF33F3DBA0D5A95F5561BAB70283AA9DAA1B12657E60BA1F3E730DCE8BA707FD4&uin=6615&fromtag=66
# https://isure.stream.qqmusic.qq.com/C400000Ka7OA0aSOGf.m4a?guid=3449912178&vkey=E8F221F7692A2365F0F3937A551E8CECE5ACAF7CEF3F5C0345C94CB2AF2D7BE19CE9B9AB5A49A3AADD73B81A727D2490452CA40E3E305CEF&uin=6615&fromtag=66
html = requests.get(url, headers=headers)
with open('test.mp4', 'wb')as f:
	f.write(html.content)