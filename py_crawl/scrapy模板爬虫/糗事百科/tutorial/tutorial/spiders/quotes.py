# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/page/1/',
                  'http://quotes.toscrape.com/page/2/']

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'quotes_text_{}.txt'.format(page)
        with open(filename, 'w')as f:
            quotes = response.css('.quote')

            for quote in quotes:
                text = quote.css('.text::text')[0].extract()
                auther = quote.css('.author::text')[0].extract()
                tags = quote.css('.tag::text').extract()
                print(text)
                print(auther)
                f.write('text:{}\nauther:{}\ntags:'.format(text,auther))
                for tag in tags:
                    print(tag)
                    f.write('{} '.format(tag))
                f.write('\n\n')