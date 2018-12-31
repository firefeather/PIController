# -*- coding: utf-8 -*-
# 爬取feebuf安全新闻

from fetch import get
import re
url = 'https://www.freebuf.com/clipped?pg=1'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/68.0.3440.106 Safari/537.36'}

def getNews():
    res = get(url,headers=headers,text=True)
    news = re.findall('<h5><a href=\"javascript:void\(0\)\">(.*?)</a></h5>.*?<div class="bugs-text">(.*?)<a href="(.*?)" target="_blank">\[(.*?)\]</a>',res,re.S)
    res = ''
    for i in range(10):
        res += '★'+news[i][0]+'\n'
        res += news[i][1]+'\n'
        res += news[i][2]+'\n'
        res += '新闻来源：'+news[i][3]+'\n\n'
    res = res.replace('\r\n','')
    res = res+'7x24快讯 from freebuf.com'
    return res

if __name__ == '__main__':
    res = getNews()
    print(res)




