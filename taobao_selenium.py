# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 17:11:20 2018

@author: weiro
"""
# 导入包
from selenium import webdriver
# 初始化 chrome
driver = webdriver.Chrome()
driver.get('https://www.taobao.com/')
print(driver.current_url)
inputTag = driver.find_element_by_name('q')
inputTag.send_keys('鞋子')

btnTag = driver.find_element_by_class_name('btn-search tb-bg')
btnTag.click()
