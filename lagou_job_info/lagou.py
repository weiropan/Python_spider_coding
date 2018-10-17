# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 21:35:14 2018
@author: weiro
"""
# 爬取拉勾网杭州站 爬虫工程师 前两页职位信息
# 保存为 csv 文件
# 网页地址 ：https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB%E5%B7%A5%E7%A8%8B%E5%B8%88?city=%E6%9D%AD%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput=


import requests
import pandas as pd



def get_info(data):
    url = "https://www.lagou.com/jobs/positionAjax.json?city=%E6%9D%AD%E5%B7%9E&needAddtionalResult=false"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
           'Referer':'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB%E5%B7%A5%E7%A8%8B%E5%B8%88?city=%E6%9D%AD%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput='
           }
    resp = requests.post(url,headers=headers,data=data)
    # 如果是json数据，直接可以调用json方法
    f = resp.json()
    return(f['content']['positionResult']['result'])



datas = [{'first':'true','pn':1,'kd':'爬虫工程师'},{'first':'false','pn':2,'kd':'爬虫工程师'},{'first':'false','pn':3,'kd':'爬虫工程师'}]
job_info_list = []
for data in datas:
    f = get_info(data)
    job_info_list.extend(f)


df = pd.DataFrame(job_info_list)
df.to_csv("job_list.csv",encoding='gb18030')
print('finished!')
