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

from selenium import webdriver
from    selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging
from urllib.parse import urljoin
from os import makedirs
from os.path import exists
from mongo_db import db
import json

# 日志基类配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s-%(levelname)s:%(message)s')
# 主页url
INDEX_URL = 'https://dynamic2.scrape.cuiqingcai.com/page/{page}'
# 超时时间
TIME_OUT = 10
# 总共的页数
TOTAL__PAGE = 10
# 存放结果的文件夹
RESULTS_DIR = 'movies'

# 不存在则创建文件夹
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

# 创建浏览器对象
browser = webdriver.Chrome('/Users/lemoncc/Documents/crawl/chromedriver/chromedriver')
# 设置等待超时对象
wait = WebDriverWait(browser, TIME_OUT)
# MongoDB数据库的集合
collection = db.moviesScrape


def scrape_page(url, condition, locator):
	"""
	定位, 并测试是否能定位到
	:param url: url
	:param condition: 需要定位的类型
	:param locator: 需要定位的地方
	:return: None
	"""
	logging.info('scraping %s', url)
	try:
		browser.get(url)
		wait.until(condition(locator))
	except TimeoutException:
		logging.error('error occurred while scraping %s', url, exc_info=True)


def scrape_index(page):
	"""
	查看是否能定位到每一页的项目
	:param page: 页数
	:return: None
	"""
	url = INDEX_URL.format(page=page)
	scrape_page(url, condition=EC.visibility_of_all_elements_located,
	            locator=(By.CSS_SELECTOR, '#index .item'))


def parse_index():
	"""
	解析页面, 获取每一页的url
	:return: None
	"""
	elements = browser.find_elements_by_css_selector('#index .item .name')
	# print(elements)
	for element in elements:
		href = element.get_attribute('href')
		yield urljoin(INDEX_URL, href)


def scrape_detail(url):
	"""
	查看是否能定位到每一个电影的名称
	:param url: 每一个电影的url
	:return: None
	"""
	scrape_page(url, condition=EC.visibility_of_element_located,
	            locator=(By.TAG_NAME, 'h2'))


def parse_detail():
	"""
	解析得到的页面
	:return: {dict} 得到的数据
	"""
	url = browser.current_url
	name = browser.find_element_by_tag_name('h2').text
	categories = [element.text for element in browser.find_elements_by_css_selector('.categories button span')]
	cover = browser.find_element_by_css_selector('.cover').get_attribute('src')
	score = browser.find_element_by_class_name('score').text
	drama = browser.find_element_by_css_selector('.drama p').text
	return {
		'url': url,
		'name': name,
		'categories': categories,
		'cover': cover,
		'score': score,
		'drama': drama
	}


def main():
	"""
	运行函数
	:return: None
	"""
	try:
		for page in range(1, TOTAL__PAGE + 1):
			scrape_index(page)
			detail_urls = parse_index()
			for detail_url in list(detail_urls):
				logging.info('details urls %s', list(detail_urls))
				scrape_detail(detail_url)
				detail_data = parse_detail()
				logging.info('detail data %s', detail_data)
				save_json(detail_data)
				save_db(detail_data)
	finally:
		browser.close()


def save_json(data):
	"""
	保存为json格式的文件
	:param data: 数据
	:return: None
	"""
	name = data.get('name')
	data_path = f'{RESULTS_DIR}/{name}.json'
	json.dump(data, open(data_path, 'w', encoding='utf8'), ensure_ascii=False, indent=2)


def save_db(data):
	"""
	保存在MongoDB里面
	:param data: 数据
	:return: None
	"""
	collection.insert_one(data)


if __name__ == '__main__':
	main()