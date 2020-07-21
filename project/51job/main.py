from jieba_tongji import TongJi
from spider import Spider


def main():
    spider = Spider()
    spider.run()
    tongJi = TongJi()
    tongJi.run()


if __name__ == '__main__':
    main()
