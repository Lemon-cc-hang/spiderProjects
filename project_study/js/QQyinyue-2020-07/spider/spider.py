import requests
import bs4
import execjs
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from urllib.parse import quote
import urllib
from pprint import pprint
from qqyinyue_db import SQLSession, Song
import os


class Spider(object):
    def __init__(self):
        headers = {'referer': 'https://y.qq.com/portal/singer_list.html'}
        self.session = requests.session()
        self.session.headers = headers
        with open('../store/singers.txt', 'w', encoding='utf8'):
            pass

    def __myProcess(self):
        # 把歌手按照首字母分成27类
        with ProcessPoolExecutor(max_workers=27)as p:
            for i in range(1, 28):
                p.submit(self.__get_singer_mid(i))

    def __getSign(self, data):
        with open('../sign/sign.js', 'r', encoding='utf8')as f:
            content = f.read()
        jsData = execjs.compile(content)
        sign = jsData.call('getSign', data)
        return sign

    def __get_singer_mid(self, i):
        data = '{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer",' \
               '"method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,"index": %s ,' \
               '"sin":0,"cur_page":1}}}'% str(i)

        sign = self.__getSign(data)
        url = "https://u.y.qq.com/cgi-bin/musics.fcg?&sign={}&data={}".format(sign, quote(data))
        html = self.session.get(url)
        # pprint(html.json())
        total = html.json()['singerList']['data']['total']
        pages = int(total)// 80
        thread_number = pages
        Thread = ThreadPoolExecutor(max_workers=thread_number)

        sin = 0
        for page in range(1, pages):
            data = '{"comm":{"ct":24,"cv":0},"singerList":{"module":"Music.SingerListServer",' \
               '"method":"get_singer_list","param":{"area":-100,"sex":-100,"genre":-100,"index":%s ' \
                   ',"sin":%s,"cur_page":%s}}}'% (str(i), str(sin), str(page))
            sign = self.__getSign(data)
            url = "https://u.y.qq.com/cgi-bin/musics.fcg?&sign={}&data={}".format(sign, quote(data))
            html = self.session.get(url).json()
            sings = html['singerList']['data']['singerlist']
            for sing in sings:
                singer_country = sing['country']
                singer_name = sing['singer_name']
                Thread.submit(self.__get_singer_data, mid=sing['singer_mid'], singer_name=singer_name, singer_country=singer_country)

            sin += 80

    def __get_singer_data(self, mid, singer_name, singer_country):
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                   'referer': 'https://y.qq.com/n/yqq/singer/003DBAjk2MMfhR.html'}
        data = '{"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList","param":{"order":1,"singerMid":"%s","begin":0,"num":10},"module":"musichall.song_list_server"}}'% mid
        sign = self.__getSign(data)
        url = 'https://u.y.qq.com/cgi-bin/musics.fcg?sign={}&data={}'.format(sign, quote(data))
        html = self.session.get(url, headers=headers).json()
        songs_num = int(html['singerSongList']['data']['totalNum'])
        datas = {}
        datas['singer_name'] = singer_name
        datas['singer_country'] = singer_country
        datas['songs_num'] = songs_num
        self.dbSession = SQLSession()

        if songs_num <= 80:
            data = '{"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList",' \
                   '"param":{"order":1,"singerMid":"%s","begin":0,"num":%s},' \
                   '"module":"musichall.song_list_server"}}' % (mid, str(songs_num))
            url = 'https://u.y.qq.com/cgi-bin/musics.fcg?sign={}&data={}'.format(sign, quote(data))
            contents = self.session.get(url, headers=headers).json()
            songs_list = []
            for song in contents['singerSongList']['data']['songList']:
                inner_song = {}
                inner_song['songname'] = song['songInfo']['name']
                inner_song['albumname'] = song['songInfo']['album']['name']
                singer = []
                for s in song['songInfo']['singer']:
                    singer.append(s['name'])
                inner_song['singer_name'] = '|'.join(singer)
                songs_list.append('inner_song')
                datas['song_mid'] = song['songInfo']['mid']
                if not inner_song['songname']:
                    inner_song['songname'] = 'None'
                if not datas['song_mid']:
                    datas['song_mid'] = 'None'
                if not inner_song['singer_name']:
                    inner_song['singer_name'] = 'None'
                if not inner_song['albumname']:
                    inner_song['albumname'] = 'None'
                # self.__download(datas['song_mid'], inner_song['songname'])
                try:
                    self.dbSession.add(Song(
                        song_name=inner_song['songname'],
                        song_mid=datas['song_mid'],
                        song_singer=inner_song['singer_name'],
                        song_ablum=inner_song['albumname']
                    ))
                    self.dbSession.commit()
                    print('[COMMIT]．．．')
                except:
                    self.dbSession.rollback()
                    print('[ROLLBACK]．．．')
            datas['sings'] = songs_list
            self.__write_txt(str(datas))
            print(datas)
        else:
            songs_list = []
            for a in range(0, songs_num, 80):
                data = '{"comm":{"ct":24,"cv":0},"singerSongList":{"method":"GetSingerSongList",' \
                       '"param":{"order":1,"singerMid":"%s","begin":%d,"num":80},' \
                       '"module":"musichall.song_list_server"}}' % (mid, int(a))
                url = 'https://u.y.qq.com/cgi-bin/musics.fcg?sign={}&data={}'.format(sign,quote(data))
                contents = self.session.get(url, headers=headers).json()
                for song in contents['singerSongList']['data']['songList']:
                    inner_song = {}
                    inner_song['songname'] = song['songInfo']['name']
                    inner_song['albumname'] = song['songInfo']['album']['name']
                    singer = []
                    for s in song['songInfo']['singer']:
                        singer.append(s['name'])
                    inner_song['singer_name'] = '|'.join(singer)
                    songs_list.append('inner_song')
                    datas['song_mid'] = song['songInfo']['mid']
                    if not inner_song['songname']:
                        inner_song['songname'] = 'None'
                    if not datas['song_mid']:
                        datas['song_mid'] = 'None'
                    if not inner_song['singer_name']:
                        inner_song['singer_name'] = 'None'
                    if not inner_song['albumname']:
                        inner_song['albumname'] = 'None'
                    # self.__download(datas['song_mid'], inner_song['songname'])
                    try:
                        self.dbSession.add(Song(
                            song_name=inner_song['songname'],
                            song_mid=datas['song_mid'],
                            song_singer=inner_song['singer_name'],
                            song_ablum=inner_song['albumname']
                        ))
                        self.dbSession.commit()
                        print('[COMMIT]．．．')
                    except:
                        self.dbSession.rollback()
                        print('[ROLLBACK]．．．')
            datas['sings'] = songs_list
            self.__write_txt(str(datas))
            print(datas)

    def __download(self, song_mid, song_name):
        headers = {
            'cookie': 'pgv_pvi=1658514432; RK=qQwsm86yR1; '
                      'ptcz=c2555f5a08ebb09541d645152b8eb7f0731d77a0ae3d0a20b5fee398760a3ea2; '
                      'pgv_pvid=3449912178; skey=@teC22CK1J; pgv_si=s2309940224; '
                      'pgv_info=ssid=s785782265; ts_refer=www.google.com.hk/; ts_uid=7747570870; '
                      'userAction=1; yqq_stat=0; player_exist=1; qqmusic_fromtag=66; '
                      'psrf_qqrefresh_token=41BA7069ECE263DB3D879F401C02F9C8; '
                      'psrf_musickey_createtime=1593236318; '
                      'qqmusic_key=Q_H_L_2urssx50eWDGVC5uP_D_ysxCKkG'
                      '-LFQ3ZkkCMQKWzgpzsukuONpAz9RGDd06jj8; tmeLoginType=2; uin=4831703; '
                      'psrf_qqopenid=331F40A04A05EC1494E427EA7E406767; euin=7ecioKSzoz**; '
                      'qm_keyst=Q_H_L_2urssx50eWDGVC5uP_D_ysxCKkG'
                      '-LFQ3ZkkCMQKWzgpzsukuONpAz9RGDd06jj8; '
                      'psrf_qqaccess_token=4F09ED9998363682A8AF40DD0CCDD504; '
                      'psrf_qqunionid=A6391CE6D325C05177B721D6C301A67A; '
                      'psrf_access_token_expiresAt=1601012318; '
                      'ts_last=y.qq.com/n/yqq/song/000Ka7OA0aSOGf.html; yplayer_open=1; yq_index=0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 ('
                          'KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'referer': 'https://y.qq.com/portal/player.html'}
        data = '{"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{' \
               '"guid":"3449912178","calltype":0,"userip":""}},"req_0":{' \
               '"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"3449912178",' \
               '"songmid":["%s"],"songtype":[0],"uin":"4831703","loginflag":1,"platform":"20"}},' \
               '"comm":{"uin":4831703,"format":"json","ct":24,"cv":0}}' % song_mid
        url = 'https://u.y.qq.com/cgi-bin/musics.fcg?sign={}&loginUin=4831703&hostUin=0&data={}'.format(
            self.__getSign(data), quote(data))
        html = requests.get(url, headers=headers)
        _url = html.json()['req_0']['data']['midurlinfo'][0]['purl']
        # pprint(_url)
        url = urllib.parse.urljoin('https://isure.stream.qqmusic.qq.com/', _url)
        html = requests.get(url, headers=headers)
        with open('../songs/{}.mp4'.format(song_name), 'wb')as f:
            f.write(html.content)

    def __write_txt(self, row):
        with open('../store/singers.txt', 'a+', encoding='utf8')as f:
            f.write(row + '\n')

    def run(self):
        self.__myProcess()
        # self.__get_singer_mid(1)

if __name__ == '__main__':
    spider = Spider()
    spider.run()
