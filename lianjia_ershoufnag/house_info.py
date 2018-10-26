# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 22:27:55 2018

@author: weiro
"""
import requests
from lxml import etree
import sys
import pandas as pd
import time
import re


def get_page(url):
    html = requests.get(url)
    if html.status_code == 200:
        response = html.text
        return response
    else:
        print('页面错误')
        sys.exit()


def get_house_info_list(url):
    '''将每个页面中每一条二手房信息保存为一个字典'''
    house_info_list = []
    response = get_page(url)
    xml = etree.HTML(response)
    titles = xml.xpath('/html/body/div[4]/div[1]/ul/li/div[1]/div[1]/a/text()')
    blocks = xml.xpath('/html/body/div[4]/div[1]/ul/li/div[1]/div[2]/div/a/text()')
    prices = xml.xpath('/html/body/div[4]/div[1]/ul/li/div[1]/div[6]/div[1]/span/text()')
    infos = xml.xpath('/html/body/div[4]/div[1]/ul/li/div[1]/div[2]/div/text()')
    for i in range(len(infos)):
        info = infos[i]
        # 房型
        house_type_info = re.search(r'\d室\d厅', info)
        # 若在字符串中没有找到该正则表达式模式，search方法返回None
        if bool(house_type_info):
            house_type = house_type_info.group()
        else:
            house_type = ''
        # 装修情况
        house_dec_info = re.search(r'精装|简装|毛坯|其他', info)
        if bool(house_dec_info):
            house_dec = house_dec_info.group().strip()
        else:
            house_dec = ''
        # 电梯情况
        house_eleva_info = re.search(r'有电梯|无电梯', info)
        if bool(house_eleva_info):
            house_eleva = house_eleva_info.group()
        else:
            house_eleva = ''
        # 面积大小
        house_size_info = (re.search(r'(\d){,4}\.*(\d){,2}平米', info)).group()
        house_size = float(house_size_info[:-2])
        # 小区名
        block = blocks[i].strip()
        # 标题
        title = titles[i].strip()
        # 价格
        price = float(prices[i].strip())
        # 添加到列表中
        house_info_list.append({'title': title,
                                'block': block,
                                'price': price,
                                'house_type': house_type,
                                'house_size': house_size,
                                'house_dec': house_dec,
                                'house_eleva': house_eleva
                                })
    return house_info_list


# 读取指定数量的页面
def house(url, pages):
    print("共需爬取%s页:" % pages)
    house_info_list = []
    for i in range(pages):
        new_url = url + 'pg%s/' % (i + 1)
        house_info_list.extend(get_house_info_list(new_url))
        time.sleep(2)
        print('\t已爬取第%s页' % (i + 1))
    return house_info_list


if __name__ == '__main__':
    url = 'https://gz.lianjia.com/ershoufang/tianhe/'
    # 将二手房信息保存到 house.xlsx文件中
    df = pd.DataFrame(house(url, 5))
    df.to_excel('tianhe.xlsx')
    print('finished!')
