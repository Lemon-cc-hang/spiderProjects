# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       spider.py
   Description :
   Author :         lemoncc
   date:            2020/7/8
-------------------------------------------------
"""
__author__ = 'lemoncc'

from pyppeteer import launch
import logging
import asyncio
import json
from os import makedirs
from os.path import exists
from mongo_db import db


class Spider(object):
	async def __init(self):
		"""
		初始化
		:return: None
		"""
		# 存放数据的路径
		self.RESULTS_DIR = 'data'
		# 检查是否存在路径, 如果没有则创建
		exists(self.RESULTS_DIR) or makedirs(self.RESULTS_DIR)
		# 存放数据 ---- MongoDB的集合
		self.collection = db.moviesScrape2
		# 日志的配置
		logging.basicConfig(level=logging.INFO,
		                    format='%(asctime)s-%(levelname)s:%(message)s')
		# 主url
		self.INDEX_URL = 'https://dynamic2.scrape.cuiqingcai.com/page/{page}'
		# 超时时间
		self.TIMEOUT = 10
		# 总共的页数
		self.TOTAL_PAGE = 10
		# 窗口显示的大小
		WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
		# pyppeteer的参数
		params = {
			'headless': False,
			'args': ['--disable-infobars', f'--window-size={WINDOW_WIDTH}, {WINDOW_HEIGHT}'],
		}
		# 创建浏览器对象
		self.browser = await launch(**params)
		# 创建一个项目对象
		self.tab = await self.browser.newPage()
		# 设置文本显示大小
		await self.tab.setViewport({'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT})

	async def scrape_page(self, url, selector):
		"""
		检查是否能定位到
		:param url: url
		:param selector: 需要定位的元素
		:return: None
		"""
		logging.info('scraping %s', url)
		try:
			await self.tab.goto(url)
			await self.tab.waitForSelector(selector, options={
				'timeout': self.TIMEOUT * 1000
			})
		except TimeoutError:
			logging.error('error occurred while scraping %s', url, exc_info=True)

	async def scrape_index(self, page):
		"""
		检查能否定位到项目
		:param page: 每一页
		:return: None
		"""
		url = self.INDEX_URL.format(page=page)
		await self.scrape_page(url, '.item .name')

	async def parse_index(self):
		"""
		返回每一页的项目的url
		:selector:      代表的是选择而的节点对应的CSS选择器
		:pageFunction:  代表的是要执行的JavaScript方法
		:return:        每一个项目的url
		"""
		return await self.tab.querySelectorAllEval('.item .name', 'nodes=>nodes.map(node=>node.href)')

	async def scrape_detail(self, url):
		"""
		检查能否定位到每一个项目的名字
		:param url: url
		:return: None
		"""
		await self.scrape_page(url, 'h2')

	async def parse_detail(self):
		"""
		解析页面, 并返回数据
		:return: {dict} 数据
		"""
		url = self.tab.url
		name = await self.tab.querySelectorEval('h2', 'node=>node.innerText')
		categories = await self.tab.querySelectorAllEval('.categories button span', 'nodes=>\
		nodes.map(node=>node.innerText)')
		cover = await self.tab.querySelectorEval('.cover', 'node=>node.src')
		score = await self.tab.querySelectorEval('.score', 'node=>node.innerText')
		drama = await self.tab.querySelectorEval('.drama p', 'node=>node.innerText')
		return {
			'url': url,
			'name': name,
			'categories': categories,
			'cover': cover,
			'score': score,
			'drama': drama
		}

	async def save_json(self, data):
		"""
		储存在json中
		:param data: 数据
		:return: None
		"""
		name = data.get('name')
		data_path = f'{self.RESULTS_DIR}/{name}.json'
		json.dump(data, open(data_path, 'w', encoding='utf8'), ensure_ascii=False, indent=2)

	async def save_db(self, data):
		"""
		存储在数据库中
		:param data: data
		:return: None
		"""
		self.collection.insert_one(data)

	async def main(self):
		"""
		启动函数
		:return: None
		"""
		await self.__init()
		try:
			for page in range(1, self.TOTAL_PAGE + 1):
				await self.scrape_index(page)
				detail_urls = await self.parse_index()
				for detail_url in detail_urls:
					await self.scrape_detail(detail_url)
					detail_data = await self.parse_detail()
					logging.info('detail_urls %s', detail_data)
					await self.save_json(detail_data)
					await self.save_db(detail_data)
		finally:
			await self.browser.close()


def spider():
	"""
	实例化
	:return: {Object}
	"""
	return Spider()


if __name__ == '__main__':
	asyncio.run(spider().main())
