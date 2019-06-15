import json,time
from fetch import post,get
from logger import Logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST='https://shareknow.xiaocong-media.com/api/'

headers={
      'User-Agent':	'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 NewsArticle/7.2.7 ToutiaoMicroApp/1.19.4.0 PluginVersion/72707',
      'referer':	'https://tmaservice.developer.toutiao.com?appid=ttdb04adb9442e6b61&version=1.3.6',
      'Content-Type':	'application/json; charset=utf-8',
      'Content-Length':	'13',
      'Host':	'shareknow.xiaocong-media.com',
      'Connection':	'Keep-Alive',
      'Accept-Encoding':	'gzip'
   }

SESSION_ID = '004f6dae060243e6931083e8b0ec54ff'

def getSmallLotteryList():
   api = HOST+'bytyluck.ashx?action=Product'
   data = {
      'PrizeId':0
   }
   response = get(api,data=data,headers=headers,verify=False)
   if not response['cdrr'] is None:
      lotteryList = response['cdrr']['a_welfare_Product']
      if not lotteryList is None:
         tryToLotteryList(lotteryList,'小抽奖')
      else:
          Logger.e('今日头条天天抽奖失败','未获取到小抽奖列表')
   else:
      Logger.n('今日头条天天抽奖失败','获取小抽奖列表失败,'+response['Msg'])

def getBigLotteryList():
   api = HOST+'bytyluck.ashx?action=StickProduct'
   data = {
      'PrizeId':0
   }
   response = get(api,data=data,headers=headers,verify=False)
   if not response['cdrr'] is None:
      lotteryList = response['cdrr']['a_welfare_Product']
      if not lotteryList is None:
         tryToLotteryList(lotteryList,'大抽奖')
      else:
          Logger.e('今日头条天天抽奖失败','未获取到大抽奖列表')
   else:
      Logger.n('今日头条天天抽奖失败','获取大抽奖列表失败,'+response['msg'])

def tryToLotteryList(lotteryList,name):
   successCount = 0
   for item in lotteryList:
       productId = item['ProductId']
       if not judgeIfIsJoined(productId):
           if(joinLotery(productId)):
               successCount+=1
   Logger.v('今日头条天天抽奖'+name+'完成,共成功参与{}次抽奖'.format(successCount))

def judgeIfIsJoined(productid):
   time.sleep(1)
   global headers
   headers['Content-Type'] = 'application/json'
   headers['Content-Length']=None
   api = HOST+'bytyluck.ashx?action=ProductDec&productid={}&sessionUserId={}'
   response = get(api.format(productid,SESSION_ID),headers=headers,verify=False)
   if not response['cdrr'] is None:
      return response['cdrr']['IsPartake'] == 1
   return False

def joinLotery(productid):
    time.sleep(1)
    global headers
    headers['Content-Type'] = 'application/json'
    headers['Content-Length']=None
    api = HOST+'bytyluck.ashx?action=JoinPartake&productid={}&sessionUserId={}'
    response = get(api.format(productid,SESSION_ID),headers=headers,verify=False)
    if response['result'] == "1":
       return True
    else:
       Logger.e('今日头条天天抽奖失败',response['msg'])
       return False


def autoJoinLottery():
    getBigLotteryList()
    getSmallLotteryList()

if __name__ == "__main__":
    autoJoinLottery()
