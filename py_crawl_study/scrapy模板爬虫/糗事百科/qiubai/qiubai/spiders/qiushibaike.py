# -*- coding: utf-8 -*-
import scrapy


class QiushibaikeSpider(scrapy.Spider):
    name = 'qiushibaike'
    allowed_domains = ['www.qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/',
                  'https://www.qiushibaike.com/text/page/2/']

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'qiushibaike_{}.html'.format(page)
        print('*'*10)
        with open(filename, 'wb')as f:
            f.write(response.body)
