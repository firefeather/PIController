
import json,time
from fetch import post,get
from logger import Logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST='https://f-pay-rp.snssdk.com/activity-service/api/lottery/'
UID=6961846004
SYS_INFO={
    "brand": "Xiaomi",
		"model": "Mi Note 3",
		"pixelRatio": 2.75,
		"screenWidth": 393,
		"screenHeight": 698,
		"windowWidth": 393,
		"windowHeight": 698,
		"statusBarHeight": 66,
		"fontSizeSetting": 33,
		"version": "7.2.7",
		"nativeSDKVersion": "2.15.0",
		"appName": "Toutiao",
		"system": "Android 8.1.0",
		"platform": "android",
		"language": "zh-CN",
		"SDKUpdateVersion": "1.19.3.4",
		"SDKVersion": "1.19.3",
		"errMsg": "getSystemInfo:ok"
}
COOKIE='odin_tt=31f588632af88e558675b71d6fc454eb3c7b0ee29b5340b2a0f6d3518b746b80237743aaa0e65410fd861047a9a9745b; UM_distinctid=16ab9241a930-017271cba8078b-5e0e767f-43113-16ab9241a9514b; sid_guard=e80cc24b3a494be29ecd88158eea5985%7C1559488803%7C5184000%7CThu%2C+01-Aug-2019+15%3A20%3A03+GMT; uid_tt=82a7d24c03110699b11a06e6aaf85ed8; sid_tt=e80cc24b3a494be29ecd88158eea5985; sessionid=e80cc24b3a494be29ecd88158eea5985; qh[360]=1; _ga=GA1.2.1073382445.1560087757; _gid=GA1.2.1247773645.1560087757; install_id=74662641983; ttreq=1$8252efe4ae79501b1c9697a42d5bf9985705c321'


def getBigLotteryList():
   headers={
      'content-type':	'application/json',
      'user-agent':	'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 NewsArticle/7.2.7 ToutiaoMicroApp/1.19.3.4 PluginVersion/72707',
      'referer':	'https://tmaservice.developer.toutiao.com?appid=ttec4d9af07367551a&version=2.5.7',
      'accept-encoding':	'gzip',
      'cookie':	COOKIE
   }
   api = HOST+'feed?ActivityShowType=LBIGIMAGE'
   response = get(api,headers=headers,verify=False)
   if response['Status']==0:
      lotteryList = response['LotteryActivityList']
      if not lotteryList is None:
          unJoinList = list(filter(lambda lottery: lottery['JoinState'] != 'JOIN', lotteryList)) or []
          successCount = 0
          for item in unJoinList:
            result = joinLotery(item['ActivityNo'])
            if result == 1:
                successCount+=1
            elif result == 3:
                Logger.v('今日头条全民大抽奖完成,共成功参与{}次抽奖'.format(successCount))
                break
            else:
                continue
      else:
          Logger.e('今日头条全民大抽奖失败','未获取到大抽奖列表')
   else:
      Logger.n('今日头条全民大抽奖失败','获取大抽奖列表失败,'+response['Msg'])

def getNewLotteryList():
   headers={
      'content-type':	'application/json',
      'user-agent':	'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 NewsArticle/7.2.7 ToutiaoMicroApp/1.19.3.4 PluginVersion/72707',
      'referer':	'https://tmaservice.developer.toutiao.com?appid=ttec4d9af07367551a&version=2.5.7',
      'accept-encoding':	'gzip',
      'cookie':	COOKIE
   }
   api = HOST+'feed?LastActivityNo='
   response = get(api,headers=headers,verify=False)
   if response['Status']==0:
      lotteryList = response['LotteryActivityList']
      if not lotteryList is None:
          unJoinList = list(filter(lambda lottery: lottery['JoinState'] != 'JOIN', lotteryList)) or []
          successCount = 0
          for item in unJoinList:
            result = joinLotery(item['ActivityNo'])
            if result == 1:
                successCount+=1
            elif result == 3:
                Logger.v('今日头条全民抽奖完成,共成功参与{}次抽奖'.format(successCount))
                break
            else:
                continue
      else:
          Logger.e('今日头条全民抽奖失败','未获取到小抽奖列表')
   else:
      Logger.n('今日头条全民抽奖失败','获取抽奖列表失败,'+response['Msg'])

def getSmallLotteryList():
    headers={
            'content-type':	'application/json',
            'user-agent':	'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 NewsArticle/7.2.7 ToutiaoMicroApp/1.19.3.4 PluginVersion/72707',
            'referer':	'https://tmaservice.developer.toutiao.com?appid=ttec4d9af07367551a&version=2.5.7',
            'accept-encoding':	'gzip',
            'cookie':	COOKIE
         }
    api = HOST+'feed'
    response = get(api,headers=headers,verify=False)
    if response['Status']==0:
       lotteryList = response['LotteryActivityList']
       if not lotteryList is None:
              unJoinList = list(filter(lambda lottery: lottery['JoinState'] != 'JOIN', lotteryList)) or []
              successCount = 0
              for item in unJoinList:
                  result = joinLotery(item['ActivityNo'])
                  if result == 1:
                      successCount+=1
                  elif result == 3:
                      Logger.v('今日头条全民小抽奖完成,共成功参与{}次抽奖'.format(successCount))
                      break
                  else:
                      continue
       else:
                Logger.e('今日头条全民小抽奖失败','未获取到小抽奖列表')
    else:
            Logger.n('今日头条全民小抽奖失败','获取抽奖小列表失败,'+response['Msg'])
      
def joinLotery(no):
    time.sleep(3)
    headers={
      'user-agent':	'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 NewsArticle/7.2.7 ToutiaoMicroApp/1.19.3.4 PluginVersion/72707',
      'referer':	'https://tmaservice.developer.toutiao.com?appid=ttec4d9af07367551a&version=2.5.7',
      'content-type':	'application/json; charset=utf-8',
      'content-length':	'460',
      'accept-encoding':	'gzip',
      'cookie':	COOKIE
   }
    api = HOST+'join'
    data='{ "ActivityNo": "%s", "JoinUid": %d, "SystemInfo": %s}' %(no,UID,json.dumps(SYS_INFO))
    response = post(api,headers=headers,data=data,verify=False)
    if response['Status'] == 0:
       return 1
    elif response['Status'] == 101:
       return 3
    else:
       Logger.e('今日头条全民抽奖失败',response['Msg'] or response['message'])
       return 2
       
def autoLottery():
   getBigLotteryList()
   getSmallLotteryList()
   getNewLotteryList()

if __name__ == "__main__":
    getLotteryList()
