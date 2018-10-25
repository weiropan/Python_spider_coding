# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 14:18:31 2018
通过控制台输入想搜索的职位及要下载的职位列表数量
@author: weiro
"""
import pandas as pd
import lagou_list
import lagou_position_desc

def main():
    data = {'first':'false',
            'pn':2,
            'kd':'文案策划'}
    data['kd'] = input('请输入您想搜索的职位名：')
    data['pn'] = int(input('请输入您想爬取的该职位列表页数：'))
    position_list = lagou_list.get_list_page(data)
    position_list = lagou_position_desc.get_positionDesc(position_list)
    df = pd.DataFrame(position_list)
    df.to_csv('%s.csv'%(data['kd']),encoding='gb18030')
    df.to_excel('%s.xlsx'%(data['kd']))
    print('数据下载完毕！')
    
if __name__=='__main__':
    main()