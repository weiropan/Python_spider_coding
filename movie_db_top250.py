# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 23:24:52 2018

@author: weiro
"""

import requests
from lxml import etree

url = 'https://movie.douban.com/top250?start=0&filter='
title_list = []

for page in range(10):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(25*page)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    html = requests.get(url,headers=headers,timeout=20).text
    xml = etree.HTML(html)
    titles = xml.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')
    title_list.extend(titles)

print(title_list)



for i in range(len(title_list)):
    print(title_list[i])