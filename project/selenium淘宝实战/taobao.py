# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       taobao.py
   Description :
   Author :         lemoncc
   date:            2020/7/8
-------------------------------------------------
"""
__author__ = 'lemoncc'

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from urllib.parse import quote
from urllib.parse import urljoin
from pyquery import PyQuery
import time

from mongo_db import db


class Taobao(object):
	def __init__(self, page):
		KEYWORD = '竖屏 2k'
		self.browser = webdriver.Chrome('/Users/lemoncc/Documents/crawl/chromedriver/chromedriver')
		self.wait = WebDriverWait(self.browser, 10)
		self.url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
		self.page = page
		self.collection = db.taobao

	def __get_html(self, page):
		try:
			self.browser.get(self.url)
			time.sleep(5)

			self.wait.until(    # 在wait的时间内等待代码的执行结束
				EC.presence_of_element_located(     # 用括号的代码定位这个元素
					(By.CSS_SELECTOR, '.m-itemlist .items .item')
				)
			)
			if page > 1:
				page_box = self.wait.until(
					EC.presence_of_element_located(
						(By.CSS_SELECTOR, 'input.input.J_Input')
					))
				submit_button = self.wait.until(
					EC.element_to_be_clickable(
						(By.CSS_SELECTOR, 'span.btn.J_Submit')
					)
				)
				page_box.clear()
				page_box.send_keys(page)
				submit_button.click()
			self.__get_content()
		except Exception as e:
			print(e)
			self.__get_html(page)

	def __get_content(self):
		# 获取源代码
		html = self.browser.page_source
		doc = PyQuery(html)
		items = doc('#mainsrp-itemlist .items .item').items()
		for item in items:
			product = {
				'image': urljoin('https://', item.find('.pic .img').attr('data-src')),
				'price': item.find('.price').text(),
				'deal': item.find('.deal-cnt').text(),
				'title': item.find('.title').text(),
				'shop': item.find('.shop').text(),
				'location': item.find('.location').text()
			}
			self.collection.insert_one(product)

	def run(self):
		for i in range(1, self.page + 1):
			self.__get_html(i)


if __name__ == '__main__':
	spider = Taobao(10)
	spider.run()