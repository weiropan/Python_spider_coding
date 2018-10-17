# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 23:24:52 2018

@author: weiro
"""

import requests
from lxml import etree
import pandas as pd

url = 'https://movie.douban.com/top250?start=0&filter='
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
           'Host':'movie.douban.com'
           }

movies_top250_list = []

for page in range(10):
    url = 'https://movie.douban.com/top250?start={}&filter='.format(25*page)
    resp = requests.get(url,headers=headers,timeout=20)
    print("第%d页响应状态码为： "%(page),resp.status_code)
    html = resp.text
    xml = etree.HTML(html)
    # 中文名
    titles = xml.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')
    # 英文名
    fore_titles = xml.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[2]/text()')
    # 导演与主演信息
    info1 = xml.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[1]')
    # 上映年份，国家，类型
    info2 = xml.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]/text()[2]')    
    # 评分
    scores = xml.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()')
 
    for i in range(len(titles)):
        title = titles[i]
        a = fore_titles[i].replace('\\xa0',' ')
        fore_title = a.split('/')[1].strip()
        
        people = info1[i].strip().split('主演:')
        director = people[0].split('导演:')[1].strip()
        star = people[-1].strip()
        score = float(scores[i].strip())
        year = info2[i].split('/')[0].strip()
        nation = info2[i].split('/')[1].strip()
        category = info2[i].split('/')[2].strip()
      
        movies_top250_list.append({'title':title,
                                   'fore_title':fore_title,
                                   'director':director,
                                   'star':star,
                                   'score':score,
                                   'year':year,
                                   'category':category,
                                   'nation':nation
                                   })
        
    print('爬取完成第%d页'%(page))


df = pd.DataFrame(movies_top250_list)
df.to_excel('movies_top250_info.xlsx')
print('爬取完成')
