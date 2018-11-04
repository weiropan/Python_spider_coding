# -*- coding: utf-8 -*-
"""
Created on 2018/10/31
@Author: weirongpan@outlook.com
@FileName: lagou_spider.py
@Software: PyCharm
程序作用：先翻页爬取拉勾网数据分析师职位列表页中职位的所有详情页链接，存入到一个列表中 然后通过遍历详情页链接爬取职位信息
"""
# 导入包
from selenium import webdriver
from lxml import etree
import time
import random
import pandas as pd

# 初始化Chrome
driver = webdriver.Chrome()
url = 'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E5%B8%88?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
driver.get(url)
# 翻页
link_list = []
while True:
    html = driver.page_source
    xml = etree.HTML(html)
    links = xml.xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[1]/div[1]/a/@href')
    next_btn = driver.find_element_by_xpath('//*[@id="s_position_list"]/div[2]/div/span[last()]')
    if 'pager_next pager_next_disabled' in next_btn.get_attribute('class'):
        break
    else:
        next_btn.click()
    link_list.extend(links)
    time.sleep(random.randint(1, 2) + random.random())  # 翻页的等待时间

psoitions = []
for link in link_list:
    driver.get(link)
    html = driver.page_source
    xml = etree.HTML(html)
    position_title = xml.xpath('/html/body/div[2]/div/div[1]/div/span/text()')[0].strip()
    salary = xml.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[1]/text()')[0].strip()
    city = xml.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[2]/text()')[0].strip()
    experience = xml.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[3]/text()')[0].strip()
    education = xml.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[4]/text()')[0].strip()
    character = xml.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[5]/text()')[0].strip()
    company = xml.xpath('//*[@id="job_company"]/dt/a/div/h2/text()')[0].strip()
    desc = "".join(xml.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()'))
    position = {'position_title': position_title,
                'salary': salary,
                'city': city,
                'experience': experience,
                'education': education,
                'character': character,
                'company': company,
                'desc': desc.strip()}
    psoitions.append(position)
    time.sleep(random.randint(1, 2) + random.random())  # 翻页的等待时间

df = pd.DataFrame(psoitions)
df.to_excel('position.xlsx')
