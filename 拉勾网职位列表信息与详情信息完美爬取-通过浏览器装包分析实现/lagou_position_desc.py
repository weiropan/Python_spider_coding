# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 14:16:02 2018
根据职位ID 获取职位详情页面职位描述信息
@author: weiro
"""
import requests
from lxml import etree
import time
import random
import lagou_list

headers = {'Cookie':'_ga=GA1.2.1428374854.1539225510; user_trace_token=20181011103830-bd39c254-ccfe-11e8-af8c-525400f775ce; LGUID=20181011103830-bd39c733-ccfe-11e8-af8c-525400f775ce; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=12; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216660fd74218dc-0da56637c0f57-9393265-1327104-16660fd742238f%22%2C%22%24device_id%22%3A%2216660fd74218dc-0da56637c0f57-9393265-1327104-16660fd742238f%22%2C%22props%22%3A%7B%22%24latest_utm_source%22%3A%22m_cf_cpt_sogou_pc%22%7D%7D; LG_LOGIN_USER_ID=9217ae28983b65567f8f3d39072d76216ced598e80a20e0d; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.531230428.1540391977; WEBTJ-ID=20181025140621-166a9d4b4715b-087ecc054c8e05-9393265-1327104-166a9d4b47c2d6; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1540441053,1540441822,1540442226,1540447582; _putrc=4628C166FF9F2E2C; JSESSIONID=ABAAABAAAGGABCBDB9815C475C090778945AD68492A99C5; login=true; unick=%E6%BD%98%E4%BC%9F%E8%8D%A3; gate_login_token=4f7a119e3d67215865c0fa0a7e68f9847a03fce10d73cf5e; _gat=1; LGSID=20181025143827-94314229-d820-11e8-9eae-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E9%25A3%258E%25E6%258E%25A7%25E5%25BB%25BA%25E6%25A8%25A1%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; TG-TRACK-CODE=search_code; SEARCH_ID=a8d58b2012ab49ee84e515030dfcd3d2; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1540449875; LGRID=20181025144436-7067f3c1-d821-11e8-9eaf-525400f775ce',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

def get_positionDesc(position_list):
    """爬取职位详情页职位描述"""
    n = 1
    for position in position_list:
        print('爬取第%s条职位描述'%n)
        positionId = position["positionId"]
        position_desc_url = 'https://www.lagou.com/jobs/%s.html'%(positionId)
        response = requests.get(position_desc_url,headers=headers)
        html = response.text
        xml = etree.HTML(html)
        positionDESC = "".join(xml.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()'))
        
        # 将职位描述信息加入到该职位字典中
        position["positionDESC"] = positionDESC.strip()
        time.sleep(random.randint(0,1)+random.random())
        n+=1
    return(position_list)


def main():
    data = {'first':'false',
            'pn':2,
            'kd':'文案策划'}
    position_list = lagou_list.get_list_page(data)
    position_list = get_positionDesc(position_list)
    # 打印展示
    i = 1
    for position in position_list:
        print(i)
        print(position)
        i+=1
    
if __name__=='__main__':
    main()