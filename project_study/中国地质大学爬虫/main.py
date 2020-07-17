from Spider.one import OneSpider
from Spider.two import TwoSpider
from Spider.three import ThreeSpider
from Spider.four import FourSpider
from Spider.five import FiveSpider
from store.store import Store
from distinguish.get_url import Get_url
from distinguish.distinguish_url2_3 import Get_url2
from distinguish.distinguish_url3_4 import Get_url3
from distinguish.distinguish_url4_5 import Get_url4
from distinguish.distinguish_url5_others import Get_url5


class Main(object):

    def __init__(self):
        self.store = Store()

    def run(self):
        print('[INFO] 正在获取教师链接．．．并区分第一系列')
        get1 = Get_url()
        get1.run()
        print('[INFO] 正在获取教师链接．．．并区分第二系列')
        get2 = Get_url2()
        get2.run()
        print('[INFO] 正在获取教师链接．．．并区分第三系列')
        get3 = Get_url3()
        get3.run()
        print('[INFO] 正在获取教师链接．．．并区分第四系列')
        get4 = Get_url4()
        get4.run()
        print('[INFO] 正在获取教师链接．．．并区分第五系列')
        get5 = Get_url5()
        get5.run()

        print('[INFO] 正在爬取第一系列．．．')
        one = OneSpider(self.store)
        one.run()
        print('[SUCCESS] 爬取成功! 一共 {} 名．．．'.format(self.store.count))
        print('[INFO] 正在爬取第二系列．．．')
        two = TwoSpider(self.store)
        two.run()
        print('[SUCCESS] 爬取成功! 一共 {} 名．．．'.format(self.store.count))
        print('[INFO] 正在爬取第三系列．．．')
        three = ThreeSpider(self.store)
        three.run()
        print('[SUCCESS] 爬取成功! 一共 {} 名．．．'.format(self.store.count))
        print('[INFO] 正在爬取第四系列．．．')
        four = FourSpider(self.store)
        four.run()
        print('[SUCCESS] 爬取成功! 一共 {} 名．．．'.format(self.store.count))
        print('[INFO] 正在爬取第五系列．．．')
        five = FiveSpider(self.store)
        five.run()
        self.store.save()
        print('[SUCCESS] 爬取成功! 一共 {} 名．．．'.format(self.store.count))


if __name__ == '__main__':
    main = Main()
    main.run()