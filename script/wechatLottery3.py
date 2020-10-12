import time
from fetch import post, get
from logger import Logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST = 'https://api-xcx.qunsou.co/xcx/lotto/'

TOKEN = 'fcd578398b3d4000bbdbbf9ef0db733f'

def getHeaders():
    return {
        'Host':
        'api-xcx.qunsou.co',
        'Connection':
        'keep-alive',
        'charset':
        'utf-8',
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 9; Mi Note 3 Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2691 MMWEBSDK/200901 Mobile Safari/537.36 MMWEBID/722 MicroMessenger/7.0.19.1760(0x27001335) Process/appbrand0 WeChat/arm64 NetType/WIFI Language/zh_CN ABI/arm64',
        'content-type':
        'application/json',
        'Accept-Encoding':
        'gzip,compress,br,deflate',
        'Referer':
        'https://servicewechat.com/wx4de13da05eaa2ef8/145/page-frame.html'
    }


global joinedCount
joinedCount = 0


def getBigLotteryListAndJoin():
    api = HOST + 'v2/sponsor/daily?access_token='+TOKEN+'&from=1'
    response = get(api, headers=getHeaders(), verify=False)
    lotteryList = response.get('data', {}).get('lotto')
    if lotteryList is None:
        Logger.e('微信抽奖工具失败', '未获取到大抽奖列表')
    else:
        joinLoterryOneByOne(lotteryList)


def getSmallLotteryListAndJoin(page=1):
    Logger.v('微信抽奖工具小抽奖获取第{}页'.format(page))
    api = HOST + 'v1/self/list?access_token='+TOKEN+'&page={}'.format(page)
    response = get(api, headers=getHeaders(), verify=False)
    lotteryList = response.get('data')
    if lotteryList is None:
        Logger.e('微信抽奖工具失败', '未获取到小抽奖列表')
    else:
        if len(lotteryList) != 0:
            joinLoterryOneByOne(lotteryList)
            getSmallLotteryListAndJoin(page+1)


def joinLoterryOneByOne(lotteryList):
    unJoinList = list(
        filter(lambda lottery: lottery.get('has_join', 1) != 1,
               lotteryList)) or []
    if len(unJoinList) != 0:
        global joinedCount
        for item in unJoinList:
            time.sleep(3)
            id = item['lid']
            if joinLotery(item['lid']):
                joinedCount += 1

def joinLotery(productId):
    api = HOST + 'v4/join'
    data ='{"lid": "'+productId+'","access_token":"'+TOKEN+'","join": 1,"join_token": "","more": 1}'
    # data ={"lid": productId,"access_token":TOKEN,"join": 1,"join_token": "","more": 1}
    response = post(api, headers=getHeaders(), data=data, verify=False)
    result = response.get('msg','error')
    if result  == '':
        return True
    else:
        Logger.e('微信抽奖工具抽奖' + productId + '失败',
                 result)
        return False


def joinWechatLottery3():
    getBigLotteryListAndJoin()
    time.sleep(5)
    getSmallLotteryListAndJoin()
    global joinedCount
    Logger.v('微信抽奖工具抽奖完毕:共成功参与{}次抽奖'.format(joinedCount))
    joinedCount = 0


if __name__ == "__main__":
    joinWechatLottery3()
