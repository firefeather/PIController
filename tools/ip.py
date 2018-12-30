# -*- coding: utf-8 -*-
# 获取服务器ip地址

import requests
import json
from fetch import get

def getServerIp():
    res = ['','','','']
    data = {'token':'70e91cd606375f987931b47290923d51'}
    url = r'http://api.ip138.com/query/'
    
    result = get(url,data)
    res[0] = result['ip']
    res[1] = result['data'][0]
    res[2] = result['data'][1] + result['data'][2] + result['data'][3]
    options = res[0] + '\n'+ res[2]
    return options
    
if __name__ =='__main__':
    res = getServerIp()
    print(res)