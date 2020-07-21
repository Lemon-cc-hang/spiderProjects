import requests

# _TODO: 1. 破解歌曲的id
# http://m10.music.126.net/20200702143424/b82448edc9c0db03705b8ae5e260fde3/yyaac/obj/wonDkMOGw6XDiTHCmMOi/3058857639/b687/e1aa/4b8f/95d75f5b0b19d9455e0e7a24f4439d4b.m4a

url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='

# _TODO: 2. - 破解params - 破解encSecKey
data = {'params': 'EmXmazG18Vz6lfvEX44H0vop+1B8PFiytEWybrJX1pqrfuhq00KCVD2yG5557xWQM/8+t80FrKyL+Q5EzN1NgyJ1hbDfeNKG8IQgfcJR7LFYGr5CPGu9XPIwtaFcbrN19TmipxtMV0CkqjxGwiT6Fg==',
        'encSecKey': '0f2d897e9cb241db3f222da324db487dbbf17f7922972c29e62accbe547d34663f7e810e7a98a32a7e51b0c545f66de67d0149528f33c987f900d28eac20fbefb671ac8fb33bef3f027f42822c06f8c96b29e78afb0e3c0347f73b40e6d55a45421bb0489c57e81a8fe0d6f9a70fe65897e9c5905bb3d009b6e8e70b7117aef2'}

html = requests.post(url, data=data)
song_url = html.json()['data'][0]['url']
html = requests.get(song_url)

with open('1.m4a', 'wb')as f:
	f.write(html.content)