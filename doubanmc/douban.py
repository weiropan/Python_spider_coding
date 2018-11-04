# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 09:48:12 2018

@author: weiro
"""
# 爬取豆瓣电影短评 后来的我们
import requests
from lxml import etree
import pandas as pd
import time
n=1
comments_list = []
headers = {'Cookie':'ll="118224"; bid=E0uYg7mAGFU; __utma=30149280.1356155306.1537320876.1537320876.1537320876.1; __utmc=30149280; __utmz=30149280.1537320876.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; __utma=223695111.1931106636.1537320876.1537320876.1537320876.1; __utmc=223695111; __utmz=223695111.1537320876.1.1.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1537320878%2C%22https%3A%2F%2Fwww.sogou.com%2Flink%3Furl%3D58p16RfDRLsoEW7-fhdQHyttFMzq2zRureaVHN88tHY.%22%5D; __yadk_uid=bVyem8WeLc3NVMPvmbojA7LTgo0KIVkC; _vwo_uuid_v2=D2BC0B0E934B2D48A38689E21324F307B|8575097d1a052222bbbdc862990a457c; ps=y; ue="15757133700@163.com"; _ga=GA1.2.1356155306.1537320876; _gid=GA1.2.1889588363.1537321208; dbcl2="183755311:tzHEMQJIPVw"; ck=2k1w; push_noty_num=0; push_doumail_num=0; __utmv=30149280.18375; _pk_id.100001.4cf6=ee7c42e444131a4f.1537320878.1.1537321359.1537320878.',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
           'X-Requested-With':'XMLHttpRequest',
           'Referer':'https://movie.douban.com/subject/26683723/comments?start=20&limit=20&sort=new_score&status=P'}

for page in range(300):
    url = 'https://movie.douban.com/subject/26683723/comments?start={}&limit=20&sort=new_score&status=P'.format(20*page)

    html = requests.get(url,headers=headers).text
    xml = etree.HTML(html)
    comments = xml.xpath('//*[@id="comments"]/div/div[2]/p/span/text()')
    authors = xml.xpath('//*[@id="comments"]/div/div[2]/h3/span[2]/a/text()')
    votes = xml.xpath('//*[@id="comments"]/div/div[2]/h3/span[1]/span/text()')
    
    for i in range(len(authors)):
        comments_dict = {}
        comments_dict['author'] = authors[i]
        comments_dict['comment'] = comments[i]
        comments_dict['vote'] = votes[i]
        comments_list.append(comments_dict)

    print('爬取完成第%s页'%n)
    n+=1
    time.sleep(2)

# 保存数据到xlsx文件
df = pd.DataFrame(comments_list)
df.to_excel('doubanmc.xlsx')



# 分词
import jieba

comment_strings=''
for i in comments_list:
    comment_strings += (i['comment'].strip())
    
seg_list = jieba.cut(comment_strings,cut_all=False) # 精确模式
split_cut ='/'.join(seg_list)

# 制作词云
from wordcloud import WordCloud
import matplotlib.pyplot as plt
wc = WordCloud(background_color = "white", #设置背景颜色  
               max_words = 2000, #设置最大显示的字数  
               margin=5,
               font_path="C:\\Windows\\Fonts\\STFANGSO.ttf",#不加这一句显示口字形乱码
               max_font_size = 80,  #设置字体最大值  
               random_state = 40, #设置有多少种随机生成状态，即有多少种配色方案  
    )  
mword =wc.generate(split_cut)
plt.imshow(mword)
plt.axis("off")
plt.show()





    
    