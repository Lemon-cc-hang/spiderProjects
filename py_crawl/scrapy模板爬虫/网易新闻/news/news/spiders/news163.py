# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from news.items import NewsItem


# https://news.163.com/20/0407/07/F9JH40SO0001899O.html
class News163Spider(CrawlSpider):
    name = 'news163'
    allowed_domains = ['news.163.com']
    start_urls = ['http://news.163.com/']

    rules = (
        Rule(LinkExtractor(allow=r'https://news.163.com/20/0425/\d+/.*?html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = NewsItem()
        item['news_thread'] = response.url.strip().split('/')[-1][:-5]
        self.get_title(response, item)
        self.get_url(response, item)
        self.get_time(response, item)
        self.get_source(response, item)
        self.get_source_url(response, item)
        self.get_body(response, item)
        return item

    def get_body(self, response, item):
        body = response.css('.post_text p::text').extract()
        if body:
            item['news_body'] = body

    def get_source_url(self, response, item):
        source_url = response.css('#ne_article_source::attr(href)').extract()
        if source_url:
            item['source_url'] = source_url

    def get_source(self, response, item):
        source = response.css('#ne_article_source::text').extract()
        if source:
            item['news_source'] = source

    def get_time(self, response, item):
        time = response.css('.post_time_source::text').extract()
        time = time[0].strip().replace('来源:', '').replace('\n', '').replace('\u3000', '')
        if time:
            item['news_time'] = time

    def get_url(self, response, item):
        url = response.url
        if url:
            # print('url:{}'.format(url))
            # print('*'*10)
            item['news_url'] = url

    def get_title(self, response, item):
        title = response.css('title::text').extract()
        if title:
            # print('title:{}'.format(title[0]))
            item['news_title'] = title[0]
        print(title)
