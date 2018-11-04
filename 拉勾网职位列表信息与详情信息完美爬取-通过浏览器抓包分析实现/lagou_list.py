# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 23:04:54 2018
获取职位列表信息
@author: weiro
"""
import requests
import time
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB%E5%B7%A5%E7%A8%8B%E5%B8%88?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
    'Cookie': '_ga=GA1.2.1428374854.1539225510; user_trace_token=20181011103830-bd39c254-ccfe-11e8-af8c-525400f775ce; LGUID=20181011103830-bd39c733-ccfe-11e8-af8c-525400f775ce; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=12; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216660fd74218dc-0da56637c0f57-9393265-1327104-16660fd742238f%22%2C%22%24device_id%22%3A%2216660fd74218dc-0da56637c0f57-9393265-1327104-16660fd742238f%22%2C%22props%22%3A%7B%22%24latest_utm_source%22%3A%22m_cf_cpt_sogou_pc%22%7D%7D; LG_LOGIN_USER_ID=9217ae28983b65567f8f3d39072d76216ced598e80a20e0d; index_location_city=%E5%85%A8%E5%9B%BD; WEBTJ-ID=20181024223936-166a6843ce4ab-079d0dc8b6c80e-9393265-1327104-166a6843ce7155; _gid=GA1.2.531230428.1540391977; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1539863439,1539925911,1539935074,1540391977; LGSID=20181024223936-a186047b-d79a-11e8-9e14-525400f775ce; PRE_UTM=m_cf_cpt_sogou_pc; PRE_HOST=www.sogou.com; PRE_SITE=https%3A%2F%2Fwww.sogou.com%2Fweb%3Fquery%3D%25E6%258B%2589%25E5%258B%25BE%26_asf%3Dwww.sogou.com%26_ast%3D%26w%3D01019900%26p%3D40040100%26ie%3Dutf8%26from%3Dindex-nologin%26s_from%3Dindex%26sut%3D3710%26sst0%3D1540391972914%26lkt%3D0%252C0%252C0%26sugsuv%3D1537265409903549%26sugtime%3D1540391972914; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_sogou_pc; _putrc=4628C166FF9F2E2C; JSESSIONID=ABAAABAAAGFABEF6F42EC4F7232601D3F22D61F711D21D9; login=true; unick=%E6%BD%98%E4%BC%9F%E8%8D%A3; gate_login_token=315b07fb028529bedd851924acfe04c4bee89144224f57c9; TG-TRACK-CODE=search_code; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1540393630; LGRID=20181024230710-7b2145a0-d79e-11e8-9e24-525400f775ce; SEARCH_ID=2c2154f9653147319d09a3590df9e16d',
    'X-Anit-Forge-Code': '0',
    'X-Anit-Forge-Token': 'None',
    'X-Requested-With': 'XMLHttpRequest'}


def get_list_page(data):
    """获取职位列表信息"""
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    # 翻页爬取
    print('爬取职位列表信息:')
    position_list = []
    for i in range(1, data['pn'] + 1):
        data['pn'] = i
        time_st = time.time()  # 当前网页开始爬取的时间
        resp = requests.post(url, headers=headers, data=data)
        # 如果是json数据，那么这个方法将会自动load成字典
        result = resp.json()
        positions = result['content']['positionResult']['result']
        for position in positions:
            # 逐条职位字典载入到职位列表中
            position_list.append(position)

        # 设置时间等待 模拟正常浏览网页的状态
        time.sleep(random.randint(1, 2) + random.random())  # 等待时间
        time_ed = time.time()  # 当前网页完成爬取的时间
        print('第{}页爬取完成，耗时：'.format(i), round(time_ed - time_st, 2), '秒')
    return (position_list)
    print('职位列表信息爬取完毕！')


def main():
    data = {'first': 'false',
            'pn': 2,
            'kd': '数据分析师'}
    position_list = get_list_page(data)
    # 打印展示
    i = 1
    for position in position_list:
        print(i)
        print(position['positionId'])
        i += 1


if __name__ == '__main__':
    main()
