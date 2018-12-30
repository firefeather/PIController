# -*- coding: utf-8 -*-
# 天气

from fetch import get
import json

global adresses
adresses = None

def getWeather(area):
    code = _getCodeByArea(area)
    if code is None:
       result = '未找到该地方'
    else:
        url = r'http://api.ip138.com/weather/'
        data = {'code':code,\
                'type':'1',\
                'callback':'find',\
                'token':'57ff2b9f0f415a5d88ec9c0e9b5c3155'
                }
        resText = get(url,data,text=True)
        res = json.loads(resText[5:-1])

        res = res['province']+res['city']+res['area'] + '\n'\
            + '===========================\n'\
            + '实时温度：'+res['data']['temp']+'摄氏度\n' \
            + '实时天气：'+res['data']['weather'] +'\n'\
            + '实时风力：'+res['data']['wind']+'\n'\
            + '湿度：'+res['data']['humidity']+'\n'\
            + 'pm2.5指数：'+res['data']['pm25']+'\n'\
            + '===========================\n'\
            + res['data']['time'] + ' from user.ip138.com'
        return res
    
def loadJson():
    try:
        with open("./tools/weatherCode.json",'r') as file:
            return json.load(file)
    except Exception:
        return {}

def _getCodeByArea(area):
    global adresses
    if adresses is None:
       adresses = loadJson()
    for key,value in adresses.items():
        if area in value:
           return key
    


if __name__  == '__main__':
    res = _getCodeByArea('洪山区')
    print(res)
