import requests
import json
from logger import Logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cookies = {
    'NTES_YD_SESS':
    'TYAM.QOaEKLc36wgIzNf3629f7Y1JCiZu8kECjGYnH69DJLIDjktuVik3_h7dJJM1h4.I8gSIzOvdTVbPBHVxDfWWEfWp84xVtycq3hZTnvmlcA57cV0WfasmJnsgKRmj_CHsXWhQgerAbxRjua4gZmF5gpzlwkrVEr0YicUYm9yE0iA2puQcm14Ad1GGrsMelTa9QeG8SiLNJ_B3q4ZCv0x1',
    '_gat':
    'GA1.2.782529179.1519958400',
    'STAREIG':
    'bc2ed0e57a1b0c7d0cc78d549c34356c4d53a45f',
    'S_INFO':
    '1519958788|0|1&65##|m18671717521',
    'P_INFO':
    'm18671717521@163.com|1519958788|1|study|00&99|sxi&1517133016&mail163#hub&420100#10#0#0|186521&1||18671717521@163.com',
    '_ntes_nnid':
    '294f702b0d1891af8c6ada01e7d2c90f,1521071927517',
    '_ntes_nuid':
    '294f702b0d1891af8c6ada01e7d2c90f',
    '_ngd_tid':
    'vrizyq4tESdsyKLGHRtAxIeMncgN5bDI',
    'mail_psc_fingerprint':
    'd7004ec5777c97e999d8f57cb0a8813e',
    'UM_distinctid':
    '1658e273979387-0c28e0368534d7-56513d62-43113-1658e27397b231',
    'NTES_YD_SESS':
    'seZmNITn6fLFgveAYiHY3Ha9eYvBQZg0cLz36WDsy31c8Ftg8d_0OTtpxtVUc7I0PBWQcNK3zpzu7uxqOFn1prKSX9LotdjK1.2e7qPlR.TjB7ukfy3Uss7xydbLntNF7goQ2JiiX6_7Pqpyolno25vBr1Zew6LigoPWItz3A1zIdIF.BD5ikH3qxMmAC3ps7zNn5ysx3d.pUXC2CH8V5b64fmUdlRF94KuccnYjFf.h.',
    'STAR_YD_SESS':
    'seZmNITn6fLFgveAYiHY3Ha9eYvBQZg0cLz36WDsy31c8Ftg8d_0OTtpxtVUc7I0PBWQcNK3zpzu7uxqOFn1prKSX9LotdjK1.2e7qPlR.TjB7ukfy3Uss7xydbLntNF7goQ2JiiX6_7Pqpyolno25vBr1Zew6LigoPWItz3A1zIdIF.BD5ikH3qxMmAC3ps7zNn5ysx3d.pUXC2CH8V5b64fmUdlRF94KuccnYjFf.h.'
}

headers = {
    'Host':
    'star.8.163.com',
    'Origin':
    'https://star.8.163.com',
    'Accept':
    'application/json, text/plain, */*',
    'User-Agent':
    'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 hybrid/1.0.0 star_client_info_begin {hybridVersion: "1.0.0",clientVersion: "1.9.0",accountId: "024ed4d78de15bc2cf623972b6dc77d26a752f5977eadbbcb91c9a4bff23c604",channel: "e01170023"}star_client_info_end',
    'Referer':
    'https://star.8.163.com/m',
    'Accept-Language':
    'zh-CN,en-US;q=0.9',
    'X-Requested-With':
    'XMLHttpRequest',
}


# 请求领取coin接口
def collectCoins(coinId):
    headers = {
        'Host':
        'star.8.163.com',
        'Accept':
        'application/json, text/plain, */*',
        'X-Requested-With':
        'XMLHttpRequest',
        'Accept-Language':
        'zh-cn',
        'Cache-Control':
        'max-age=0',
        'Content-Type':
        'application/json;charset=UTF-8',
        'Origin':
        'https://star.8.163.com',
        'User-Agent':
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Mobile/15B202star_client_1.0.0',
        'Referer':
        'https://star.8.163.com/m',
    }
    data = '{"id":%s}' % coinId
    response = requests.post(
        'https://star.8.163.com/api/starUserCoin/collectUserCoin',
        headers=headers,
        cookies=cookies,
        data=data,
        verify=False)
    result = response.json()['msg']
    if not '成功' in result:
        Logger.e('网易星球收取黑钻失败',result)

def autoCollectCoins():
    # 1、请求首页数据，检查是否有coin可以收集。有则将coin保存到列表容器
    response = requests.post(
        'https://star.8.163.com/api/home/index',
        headers=headers,
        cookies=cookies,
        verify=False)
    collectCoinsList = response.json()['data']['collectCoins']
    if len(collectCoinsList) == 0:
        Logger.v('网易星球当前没有黑钻可收取')
    else:
        # 2、检查coin列表容器是否有值，遍历请求领取coin接口
        Logger.v('共有{}个黑钻可收取'.format(len(collectCoinsList)))
        for collectCoinsItem in collectCoinsList:
            collectCoins(collectCoinsItem['id'])
        Logger.v('网易星球收取黑钻完毕')


if __name__ == "__main__":
    autoCollectCoins()
