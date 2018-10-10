# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 21:29:11 2018

@author: weiro
"""
 
# 爬取 房天下 租房数据
import requests
from lxml import etree
import pandas as pd

# 获取网页文本
def get_html_text(url):
    try:
        r = requests.get(url,timeout=20)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生异常'

# 解析网页
def anly_html_text(url):
    html = get_html_text(url)
    xml = etree.HTML(html)

    # 标题 
    #titles = xml.xpath('//*[starts-with(@id,"rentid_D09")]/a/@title')
    titles = xml.xpath('//*[contains(@id,"rentid_D09")]/a/@title')
    # 方式
    modes = xml.xpath('//*[@id="listBox"]/div[2]/dl/dd/p[2]/text()[1]')
    # 户型
    house_types = xml.xpath('//*[@id="listBox"]/div[2]/dl/dd/p[2]/text()[2]')
    # 面积
    areas = xml.xpath('//*[@id="listBox"]/div[2]/dl/dd/p[2]/text()[3]')
    # 租金
    prices = xml.xpath('//*//*[@id="listBox"]/div[2]/dl/dd/div[2]/p/span/text()')
    # 小区名
    blocks = xml.xpath('//*[starts-with(@id,"rentid_D09_")]/a[3]/span/text()')
    # 区域
    districts = xml.xpath('//*[contains(@id,"rentid_D09")]/a[1]/span/text()')
    
    return [titles,modes,house_types,areas,prices,blocks,districts]

# 打印
def print_pattern(url):
    items = anly_html_text(url)
    for item in items:
        for x in item:
            print(x)


    
if __name__=='__main__':
    url = 'http://dy.zu.fang.com/'
    #anly_html_text(url)
    print_pattern(url)