# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 22:25:15 2018

@author: weiro
"""

import district
import house_info
import pandas as pd
from xpinyin import Pinyin

p = Pinyin()
from pymongo import MongoClient

client = MongoClient()


def run(url):
    districts_url = district.anly_district_dict(url)[2]
    district_name = input("请输入您想要查询的区县名: ")
    district_name_p = p.get_pinyin(u"%s" % (district_name))
    district_url = districts_url.get(district_name)
    pages = int(input("请输入您想要爬取的网页数："))
    print("请稍等，正在为您爬取相关网页")

    # 读取网页并保存到 csv 中
    lst = house_info.house(district_url, pages)
    df = pd.DataFrame(lst)
    df.to_csv('{}.csv'.format(district_name_p), encoding='gb18030')
    print('finished!')

    # 保存到 MongoDB 数据库中
    db = client.Lianjia  # 连接 Lianjia 数据库，没有则自动创建
    myset = db.hangzhou_xihu  # 使用 hangzhou_xihu ，没有则自动创建
    myset.insert(lst)


if __name__ == "__main__":
    url = 'https://hz.lianjia.com//'  # 任意城市链家首页
    run(url)
