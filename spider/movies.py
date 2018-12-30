# -*- coding: utf-8 -*-
# 爬取猫眼电影

import re
import time
from fetch import get

def getMovies():
    url = 'http://maoyan.com/board/7'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    dataNum = time.strftime('%Y年%m月%日',time.localtime(time.time()))
    
    response = get(url,headers=headers,text=True)
    result1 = re.findall('<p class="name"><a href="(.*?)" title="(.*?)" data-act="boarditem-click" data-val=".*?">.*?</a></p>.*?<p class="star">\s+(.*?)\s+</p>.*?<p class="releasetime">(.*?)</p>    </div>.*?<div class="movie-item-number score-num">.*?<p class="score"><i class="integer">(.*?)</i><i class="fraction">(.*?)</i></p>        ',response,re.S)
    resultStr=dataNum+'最新电影排行\n===========================\n'
    n = 1
    for i in result1:
        resultStr+='★第'+str(n)+'位 '
        resultStr+=i[1]+' '
        resultStr+=i[4]+i[5]+'\n'
        resultStr+=i[2]+'\n'
        resultStr+='http://maoyan.com'+i[0]+'\n'
        resultStr+=i[3]+'\n'
        n += 1
        if(n > 10):
            # 展示前五个电影
            break
    resultStr+='===========================\n'
    resultStr+=time.strftime('%H:%M:%S',time.localtime(time.time())) + ' from maoyan.com'
    return resultStr

if __name__ == "__main__":
    print(getMovies())  
        
