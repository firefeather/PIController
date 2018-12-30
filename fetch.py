# -*- coding: utf-8 -*-
# 简单的网络请求框架

import requests,json

def postJson(url,params):
    data = json.dumps(params,ensure_ascii=False)
    print('111111111',data)
    response = requests.post(url, data)
    result = response.json()
    print('postJson:',url,params,result)
    return result

def post(url,params):
    response = requests.post(url, params)
    result = response.json()
    print('post:',url,params,result)
    return result

def getWithParams(url,params):
    response = requests.get(url, params)  
    result = response.json()
    print('getWithParams:',url,result)
    return result

def getText(url):
    response = requests.get(url)  
    result = response.text
    print('getText:',url,result)
    return result

def get(url):
    response = requests.get(url)  
    result = response.json()
    print('get:',url,result)
    return result