# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 19:27:12 2018

@author: weiro
"""
# 获取城市与区域链接

import requests
from lxml import etree


def get_citys_html(url):
    '''获取链家经营的全国城市网址'''
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except:
        return ("产生错误，错误代码: {}".format(response.status_code))


def anly_citys_url(url):
    '''解析链家经营二手房业务的全国城市网址，提取城市名与 url '''
    html = get_citys_html(url)
    xml = etree.HTML(html)
    city_names = xml.xpath('/html/body/div[11]/div/div[2]/div[1]/div[2]/div[1]/dd/a/text()')
    city_urls = xml.xpath('/html/body/div[11]/div/div[2]/div[1]/div[2]/div[1]/dd/a/@href')
    # 存储为字典格式
    print('链家在全国开展二手房业务的城市如下：')
    citys_url = {}
    for i in range(1, len(city_names)):
        citys_url[city_names[i][:-3]] = city_urls[i]
    for k, v in citys_url.items():
        print(k, v)
    return citys_url


if __name__ == "__main__":
    url = 'https://hz.lianjia.com/'
    anly_citys_url(url)
