# -*- coding: utf-8 -*-
"""
Created on 2018/10/31
@Author: weirongpan@outlook.com
@FileName: lagou.py
@Software: PyCharm
程序作用：
先爬取一页要搜索的拉勾网职位信息（如数据分析师）列表页中所有的职位详情页链接（15条），
然后遍历这15条链接进行详情页爬取，最后再切回职位信息列表页进行翻页。
"""
# 导入包
from selenium import webdriver
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import time
import pandas as pd


class Lagouspider():
    '''初始化拉勾爬虫类'''

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://www.lagou.com/jobs/list_%E9%A9%B4%E5%A6%88%E5%A6%88?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
        self.positions = []

    def run(self):
        """进行翻页的方法"""
        self.driver.get(self.url)
        while True:
            html = self.driver.page_source
            '''设置显示等待'''
            WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="s_position_list"]/div[2]/div/span[last()]'))
            )
            '''获取职位详情页链接'''
            self.get_list_links(html)
            '''进行翻页'''
            try:
                next_btn = self.driver.find_element_by_xpath('//*[@id="s_position_list"]/div[2]/div/span[last()]')

                # 判断是否为最后一页
                if "pager_next pager_next_disabled" in next_btn.get_attribute('class'):
                    break
                else:
                    next_btn.click()
            except:
                print(html)
            # 模拟人工翻页
            time.sleep(random.randint(1, 2) + random.random())

    def get_list_links(self, html):
        '''获取职位详情页的链接的方法'''
        xml = etree.HTML(html)
        links = xml.xpath('//*[@id="s_position_list"]/ul/li/div[1]/div[1]/div[1]/a/@href')
        for link in links:
            self.request_detail_page(link)
            time.sleep(random.randint(1, 2) + random.random())

    def request_detail_page(self, url):
        """请求职位详情页的方法"""
        self.driver.execute_script("window.open('%s')"%url)  # 打开一个新的页面
        self.driver.switch_to.window(self.driver.window_handles[1])  # 切换到新打开的这个页面
        WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="job_detail"]/dd[1]/p'))
        )  # 设置显示等待
        html = self.driver.page_source  # 获取详情页网页源代码
        self.get_detail_page(html)  # 爬取职位信息
        self.driver.close() # 关闭当前页面
        self.driver.switch_to.window(self.driver.window_handles[0])  # 切换回职位列表页

    def get_detail_page(self, html):
        '''解析职位详情'''
        xml = etree.HTML(html)
        salary = xml.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[1]/text()')[0].strip()      # 薪水
        city = xml.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[2]/text()')[0].strip()        # 城市
        experience = xml.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[3]/text()')[0].strip()  # 经验
        education = xml.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[4]/text()')[0].strip()   # 学历
        job_type = xml.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[5]/text()')[0].strip()
        job_desc = "".join(xml.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()'))
        company = xml.xpath('//*[@id="job_company"]/dt/a/div/h2/text()')[0].strip()
        position = {'salary': salary,
                    'city': city,
                    'experience': experience,
                    'education': education,
                    'job_type': job_type,
                    'job_desc': job_desc,
                    'company':company}
        print(position)
        self.positions.append(position)


if __name__ == '__main__':
    mylagou = Lagouspider()
    mylagou.run()
    df = pd.DataFrame(mylagou.positions)
    df.to_excel('lvmama_1.xlsx')


