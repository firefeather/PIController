import time
from fetch import post
from logger import Logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST='https://pet-chain.duxiaoman.com'

def autoCollect():
    getVigorList()
    lottery()

def getHeader(timestamp):
    return {
        'Host':	'pet-chain.duxiaoman.com',
        'Connection':	'keep-alive',
        'Content-Length':	'112',
        'Accept':'application/json',
        'Origin':	'https://pet-chain.duxiaoman.com',
        'User-Agent':'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.112 Mobile Safari/537.36 BaiduWallet-8.2.0.8-Android-walletapp_1080_1920_Mi-Note-3-jason_27_8.1.0_4.0.5_405',
        'Content-Type':	'application/json',
        'Referer':	'https://pet-chain.duxiaoman.com/',
        'Accept-Encoding':	'gzip, deflate',
        'Accept-Language':	'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie':'STDCJUVF=eyJ1YSI6IkJhaWR1V2FsbGV0LTguMi4wLjgtQW5kcm9pZC13YWxsZXRhcHBfMTA4MF8xOTIwX01pLU5vdGUtMy1qYXNvbl8yN184LjEuMF80LjAuNV80MDUiLCJjdSI6IjU0QkNFM0ZBMzM1QTZFM0QyQjZCNjU4MEVERkJDQjdDIiwiY3UyIjoiNTRCQ0UzRkEzMzVBNkUzRDJCNkI2NTgwRURGQkNCN0N8MTI2ODg3MTMwMzE0NjY4In0=; Hm_lvt_2a9b55018981a1911dd3914ca3f9bcf6={}; BDUSS=duMEUyMkJXMm1YTTZ6aktHcTdmQ09IYU1BcDE2S0UxZGV2WHFKMUM5Nm41aDVkRVFBQUFBJCQAAAAAAAAAAAEAAABki8A~T2FfZmx5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKdZ91ynWfdcUE; STOKEN=67893d44de76f46e5d8c57dd6b53767fa76df3b163b960151891b3177b398799; Hm_lpvt_2a9b55018981a1911dd3914ca3f9bcf6={}'.format(int(timestamp/1000)-3600,int(timestamp/1000)),
        'X-Requested-With':	'com.baidu.wallet'
    }

def getVigorList():
    api = HOST+'/data/vigor/generate'
    timestamp = time.time()*1000
    data = '{"requestId":%d,"appId":1,"tpl":"","timeStamp":null,"nounce":null,"token":null,"phoneType":"android"}' %timestamp
    response = post(
        api,
        headers=getHeader(timestamp),
        data=data,
        verify=False)
    print('response',response)
    if response['errorNo'] != '00':
       Logger.e('百度莱茨狗收取元气失败','错误代码'+response['errorNo'])
       return
    vigorList = response['data']['amounts']
    if len(vigorList) == 0:
        Logger.v('百度莱茨狗当前没有元气可收取')
    else:
        Logger.v('共有{}个元气可收取'.format(len(vigorList)))
        # count = 0.0
        # for vigor in vigorList:
        #     count += collectVigor(vigor)
        # Logger.v('百度莱茨狗收取元气完毕,本次收取{}颗元气'.format(count))
        collectAllVigor()

def collectVigor(id):
    time.sleep(1)
    api = HOST+'/data/vigor/get'
    timestamp = time.time()*1000
    data = '{"amount":%s,"requestId":%d,"appId":1,"tpl":"","timeStamp":null,"nounce":null,"token":null,"phoneType":"android"}' %(id ,timestamp)
    response = post(
        api,
        headers=getHeader(timestamp),
        data=data,
        verify=False)
    count = float(response['data']['amount'])
    return count

def collectAllVigor():
    time.sleep(1)
    api = HOST+'/data/vigor/getall'
    timestamp = time.time()*1000
    data = '{"requestId":%d,"appId":1,"tpl":"","timeStamp":null,"nounce":null,"token":null,"phoneType":"android"}' %timestamp
    response = post(
        api,
        headers=getHeader(timestamp),
        data=data,
        verify=False)
    amounts = response['data']['amounts']
    if len(amounts) > 0:
        count = 0.0
        for amount in amounts:
            count += float(amount)
    Logger.v('百度莱茨狗一键收取元气完毕,本次收取{}颗元气'.format(count))
        
def lottery():
    time.sleep(2)
    api = HOST+'/data/lottery/draw'
    timestamp = time.time()*1000
    data = '{"requestId":%d,"appId":1,"tpl":"","timeStamp":null,"nounce":null,"token":null,"phoneType":"android"}' %timestamp
    response = post(
        api,
        headers=getHeader(timestamp),
        data=data,
        verify=False)
    errorMsg = response['errorMsg']
    if errorMsg == 'success':
        Logger.v('百度莱茨狗抽奖成功')
    else:
        Logger.e('百度莱茨狗抽奖失败',errorMsg)


if __name__ == "__main__":
    getVigorList()
