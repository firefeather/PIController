from fetch import post
from logger import Logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

global cookie
cookie = '24s1XDhRBx7GTbouqfOLp1zxMVO2tLtp5irWPzo6LrzS.6Js.4TFkUJNSJMjLxqFGCXmLHg9WNWbxbSPk6zrNQghyva5J48grBARxPGI7BU8CxbVEc9j22xSc4eazJH6xs5mAfddylTxGPNc5Iz5AOKCQriRZladsRm8NBAgMFAPtVkqyqd3T5WRr6r0VrUufVOai5X4j4_rVnd33D9KMgwGYIBHaOBBYqwCEKovZ1eRB'

cookies = {
    'NTES_YD_SESS':
    'TYAM.QOaEKLc36wgIzNf3629f7Y1JCiZu8kECjGYnH69DJLIDjktuVik3_h7dJJM1h4.I8gSIzOvdTVbPBHVxDfWWEfWp84xVtycq3hZTnvmlcA57cV0WfasmJnsgKRmj_CHsXWhQgerAbxRjua4gZmF5gpzlwkrVEr0YicUYm9yE0iA2puQcm14Ad1GGrsMelTa9QeG8SiLNJ_B3q4ZCv0x1',
    '_ga':
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
    'NTES_YD_SESS':cookie,
    'STAR_YD_SESS':cookie,
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
        'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 hybrid/1.0.0 star_client_info_begin {hybridVersion: "1.0.0",clientVersion: "1.9.0",accountId: "024ed4d78de15bc2cf623972b6dc77d26a752f5977eadbbcb91c9a4bff23c604",channel: "e01170023"}star_client_info_end',
        'Referer':
        'https://star.8.163.com/m',
    }
    data = '{"id":%s}' % coinId
    response = post(
        'https://star.8.163.com/api/starUserCoin/collectUserCoin',
        headers=headers,
        cookies=cookies,
        data=data,
        verify=False)
    result = response['msg']
    if not '成功' in result:
        Logger.e('网易星球收取黑钻失败',result)
        return False
    return True

def autoCollectCoins():
    # 1、请求首页数据，检查是否有coin可以收集。有则将coin保存到列表容器
    response = post(
        'https://star.8.163.com/api/home/index',
        headers=headers,
        cookies=cookies,
        verify=False)
    if response['data'] is None:
        Logger.e('网易星球收取黑钻失败',response['msg'])
        if '登录失败' in response['msg']:
            Logger.n('网易星球登录失败','可能为session过期')
            getCookie()
        else:
            return
    collectCoinsList = response['data']['collectCoins']
    if len(collectCoinsList) == 0:
        Logger.v('网易星球当前没有黑钻可收取')
    else:
        # 2、检查coin列表容器是否有值，遍历请求领取coin接口
        Logger.v('共有{}个黑钻可收取'.format(len(collectCoinsList)))
        count=0.0
        for collectCoinsItem in collectCoinsList:
            if collectCoins(collectCoinsItem['id']):
               count+=float(collectCoinsItem['virCount'])
        Logger.v('网易星球收取黑钻完毕,本次收取{}颗黑钻'.format(count))

def getCookie():
    Logger.v('尝试自动更新网易星球cookie')
    data={
        'p':'SAmsdBV+moUeDdvBbRUuAc/ShOCiz6IKgs9epb6qLwBgUF7Cp9EVZhjfzpzcr4WpiWsUR8j6apiqvV6sHwGXulwTpSp/pSxFTg5IGdgCxixujZjrjphEGg8fBkaL7yf+tF/Y+WbRB9Er3wr9KvyEmsrMLuuD0KJLpLjnauZWiOMj67t/kfaSrD2Wp6t8vLOmYXktBZ3eM9jkWDQIVAwCytT041htoSg4Jr1Gd2dll/oGO32PvhtzF7gRT5foKQqEc1vK7F23+mQQmpzx1v3LVYQCLKodFix+r8S1X4T0UTtuvCwLGZSh5UIlBF5Vbory2SUasZAcFHSMG3hUsVpfNpzY6bj+lERh+ZcYlw4r9+do+1Pg8u903SFmvL4dlfYXnq+DVc8YTgExt0TROQMfpw==',
        'k':'b4h+FNm0kIztyRd25ADGo8tGQMufNy+WW3Kuf4/kI3cIvCQ9jx/DFu9iWVm6w/qVQufzVDo9ULepwHhfymGhkUGbt8Bype6LE0UyW0j4icz0ttV2UdWxWl3UymL9+A3hJgiqs77bfBO8B+jgKe+elBjfTq4f4zKpeKdtAwxEEZo='
    }
    response = post(
        'https://star.8.163.com/api/starUser/getCookie',
        data,
        headers=headers,
        cookies=cookies,
        verify=False)
    newCookie = response['data']['cookie']
    if not newCookie is None:
        global cookie
        cookie = newCookie
        Logger.v('已自动更新网易星球cookie')
    

if __name__ == "__main__":
    autoCollectCoins()
