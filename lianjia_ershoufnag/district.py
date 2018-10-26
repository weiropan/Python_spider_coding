# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 20:06:23 2018

@author: weiro
"""
from lxml import etree
import citys


def get_city_url(url):
    '''根据输入的城市名查得该城市网址'''
    citys_url = citys.anly_citys_url(url)
    city_name = input("请输入您想查询的城市:")
    city_url = citys_url.get(city_name)
    print(city_name, city_url)
    print("%s有以下区县：" % (city_name))
    return city_url


def anly_district_dict(url):
    '''根据输入城市生成二手房区域url字典'''
    city_url = get_city_url(url)
    city_esf_url = city_url + 'ershoufang/'
    b_html = citys.get_citys_html(city_esf_url)
    xml = etree.HTML(b_html)
    district_names = xml.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a/text()')
    district_urls_s = xml.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a/@href')
    # 存储为字典格式
    districts_url = {}
    for i in range(len(district_names)):
        districts_url[district_names[i]] = city_url[:-1] + district_urls_s[i]
    # 打印区县名及url
    for k, v in districts_url.items():
        print('\t', k, v)
    return (city_url, city_esf_url, districts_url)


if __name__ == "__main__":
    url = 'https://hz.lianjia.com/'
    anly_district_dict(url)
