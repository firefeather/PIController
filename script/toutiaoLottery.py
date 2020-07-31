
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

COOKIE='odin_tt=1313a030eb3119e5511889fee693319a6b1b28989f6a5675cc79b09c88044fdd7d68a7f3d3c92d0d43d150c49a40c13e; UM_distinctid=171cfedbe801b2-001d3a7dc6925a-53716a3c-448e0-171cfedbe8174; uid_tt=3a02bbbd68b6590b8834103684ace876; sid_tt=f22eedbba6526244303c201cb9a9b966; sessionid=f22eedbba6526244303c201cb9a9b966; WIN_WH=360_701; uid_tt_ss=3a02bbbd68b6590b8834103684ace876; sessionid_ss=f22eedbba6526244303c201cb9a9b966; tt_webid=6838452588007654926; PIXIEL_RATIO=3; qh[360]=1; sid_guard=f22eedbba6526244303c201cb9a9b966%7C1595406445%7C5184000%7CSun%2C+20-Sep-2020+08%3A27%3A25+GMT; install_id=3834692842032852; ttreq=1$9a38750839db1171f71c5ff22f50f18c0c90cf78; history=alrvlFic6pJZXJCTWBmSmZt6KV45U2qpZ0lqbvE9BoHLDKyftCb2NvBfEg5jOXA5Xjm%2B4wQDE8cldg4GB5Cc8CzlAt5LfAIgOaVVP5sbmFguCU5hcLgcrzRRfakDE%2B8lrh4QTzn%2Bo1lTE%2F8lUQmwXCnn0VYmjkusbmDeiV3vmJr4Londgpip8vndFf5LzC0sB0A8k0dBDDyXOE6BbTiVzO3UxHuJxw%2Bs73B1HAMT3yX%2BS2AbMgRamZq4L0nMYQi4HK8YnXrZgYnnEgMDWK5%2Bs03DIb5LUnEgOaWjumkNTNyXGA8xOAAAAAD%2F%2Fw%3D%3D'

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
          if len(unJoinList) == 0:
              Logger.e('今日头条全民大抽奖','没有未参加的大抽奖项目')
          else:
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
