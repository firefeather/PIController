# -*- coding: utf-8 -*-
# 有道翻译

import json
from fetch import get

def translate(txt):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = {
        'from':'AUTO',
        'to':'AUTO',
        'smartresult':'dict',
        'client':'fanyideskweb',
        'salt':'1500092479607',
        'sign':'c98235a85b213d482b8e65f6b1065e26',
        'doctype':'json',
        'version':'2.1',
        'keyfrom':'fanyi.web',
        'action':'FY_BY_CL1CKBUTTON',
        'typoResult':'false',
        'i':txt
        }
    result = get(url,data)
    res = '翻译结果:%s '% (result['translateResult'][0][0]['tgt'])
    return res

if __name__ == '__main__':
    print(translate(input('输入需要翻译的词或者句子：')))
                

