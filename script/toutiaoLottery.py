import json, time
from fetch import post, get
from logger import Logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST = 'https://f-pay-rp.snssdk.com/activity-service/api/lottery/'
UID = 6961846004
SYS_INFO = {
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
cookies = [
    'uid_tt=6853de0ae0904662fdf0650546b5f664; uid_tt_ss=6853de0ae0904662fdf0650546b5f664; sid_guard=c045c894baeaa9ef493c5dc5734d241a%7C1599545553%7C5183940%7CSat%2C+07-Nov-2020+06%3A11%3A33+GMT; sid_tt=c045c894baeaa9ef493c5dc5734d241a; sessionid=c045c894baeaa9ef493c5dc5734d241a; sessionid_ss=c045c894baeaa9ef493c5dc5734d241a; odin_tt=a327c2401c69bd0c7120fbf8e39f841064dfe8bec4283803f8c48843cf5d997e7b5ef8abaa76b56d1ae500f43518dc58; qh[360]=1',
    'uid_tt=58fa1bad690855f2468f92258a9dbb43; uid_tt_ss=58fa1bad690855f2468f92258a9dbb43; sid_guard=dec56af4306f93b60e50572c320fbc9c%7C1599547313%7C5182483%7CSat%2C+07-Nov-2020+06%3A16%3A36+GMT; install_id=2550478048603880; sid_tt=dec56af4306f93b60e50572c320fbc9c; ttreq=1$a98281a0270af8a62da3d8b44b1cef2505765840; sessionid=dec56af4306f93b60e50572c320fbc9c; sessionid_ss=dec56af4306f93b60e50572c320fbc9c; odin_tt=6ff06923d5c7400978c2cfebaec0a62392eb9a21b438977cd55d5a070ac9ee5aa27c5e216f6689019b23ba495ab17655; qh[360]=1'
]

global COOKIE

def getHeaders():
    return {
    'content-type':
    'application/json',
    'user-agent':
    'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 NewsArticle/7.2.7 ToutiaoMicroApp/1.19.3.4 PluginVersion/72707',
    'referer':
    'https://tmaservice.developer.toutiao.com?appid=ttec4d9af07367551a&version=2.5.7',
    'accept-encoding':
    'gzip',
    'cookie':
    COOKIE
}

def getBigLotteryList():
    api = HOST + 'feed?ActivityShowType=LBIGIMAGE'
    response = get(api, headers=getHeaders(), verify=False)
    if response['Status'] == 0:
        lotteryList = response['LotteryActivityList']
        if not lotteryList is None:
            unJoinList = list(
                filter(lambda lottery: lottery['JoinState'] != 'JOIN',
                       lotteryList)) or []
            if len(unJoinList) == 0:
                Logger.e('今日头条全民大抽奖', '没有未参加的大抽奖项目')
            else:
                successCount = 0
                for item in unJoinList:
                    result = joinLotery(item['ActivityNo'])
                    if result == 1:
                        successCount += 1
                    elif result == 3:
                        Logger.v('今日头条全民大抽奖完成,共成功参与{}次抽奖'.format(successCount))
                        break
                    else:
                        continue
        else:
            Logger.e('今日头条全民大抽奖失败', '未获取到大抽奖列表')
    else:
        Logger.n('今日头条全民大抽奖失败', '获取大抽奖列表失败,' + response['Msg'])


global shouldGetMore  #是否加载更多
shouldGetMore = True


def getNewLotteryList(lastActivityNo=''):
    api = HOST + 'feed?LastActivityNo=' + lastActivityNo
    response = get(api, headers=getHeaders(), verify=False)
    if response['Status'] == 0:
        lotteryList = response['LotteryActivityList']
        if not lotteryList is None:
            unJoinList = list(
                filter(lambda lottery: lottery['JoinState'] != 'JOIN',
                       lotteryList)) or []
            global shouldGetMore
            if len(unJoinList) == 0:
                if shouldGetMore:
                    getNewLotteryList(lotteryList[-1]['ActivityNo'])
                return
            successCount = 0
            for item in unJoinList:
                result = joinLotery(item['ActivityNo'])
                if result == 1:  #成功
                    successCount += 1
                elif result == 3:  #被限制
                    shouldGetMore = False
                    Logger.v('今日头条全民抽奖完成,共成功参与{}次抽奖'.format(successCount))
                    break
                else:  #未知原因失败了
                    continue
            if shouldGetMore:
                getNewLotteryList(lotteryList[-1]['ActivityNo'])
            else:
                shouldGetMore = True
        else:
            Logger.e('今日头条全民抽奖失败', '未获取到小抽奖列表')
    else:
        Logger.n('今日头条全民抽奖失败', '获取抽奖列表失败,' + response['Msg'])


def getSmallLotteryList():
    api = HOST + 'feed'
    response = get(api, headers=getHeaders(), verify=False)
    if response['Status'] == 0:
        lotteryList = response['LotteryActivityList']
        if not lotteryList is None:
            unJoinList = list(
                filter(lambda lottery: lottery['JoinState'] != 'JOIN',
                       lotteryList)) or []
            if len(unJoinList) == 0:
                Logger.e('今日头条全民小抽奖', '没有未参加的小抽奖项目')
            return
            successCount = 0
            for item in unJoinList:
                result = joinLotery(item['ActivityNo'])
                if result == 1:
                    successCount += 1
                elif result == 3:
                    Logger.v('今日头条全民小抽奖完成,共成功参与{}次抽奖'.format(successCount))
                    break
                else:
                    continue
        else:
            Logger.e('今日头条全民小抽奖失败', '未获取到小抽奖列表')
    else:
        Logger.n('今日头条全民小抽奖失败', '获取抽奖小列表失败,' + response['Msg'])


def joinLotery(no):
    time.sleep(3)
    api = HOST + 'join'
    data = '{ "ActivityNo": "%s", "JoinUid": %d, "SystemInfo": %s}' % (
        no, UID, json.dumps(SYS_INFO))
    response = post(api, headers=getHeaders(), data=data, verify=False)
    if response['Status'] == 0:
        return 1
    elif response['Status'] == 101:
        return 3
    else:
        Logger.e('今日头条全民抽奖失败', response['Msg'] or response['message'])
        return 2


def autoLottery():
    global COOKIE
    for cookie in cookies:
        COOKIE = cookie
        Logger.v('今日头条全民抽奖用户抽奖:' + COOKIE[0:15])
        autoUserLottery()


def autoUserLottery():
    getMoreChance()
    getBigLotteryList()
    getSmallLotteryList()
    getNewLotteryList()


def getMoreChance():
    api = HOST + 'query-activity-task'
    response = get(api, headers=getHeaders(), verify=False)
    if response['Code'] == '0':
        taskList = response['TaskInfos']
        if not taskList is None:
            if len(taskList) == 0:
                Logger.v('今日头条全民抽奖增加次数失败:没有可以完成的任务')
                return
            successCount = 0
            for item in taskList:
                rewardCount = int(item['RewardChance'])
                times = 5
                id = item['TaskNo']
                for i in range(0, times):
                    time.sleep(3)
                    if _finishTask(id):
                        successCount += rewardCount
                    else:
                        break
                    time.sleep(5)
            Logger.v('今日头条全民抽奖成功增加%d次数' % successCount)
        else:
            Logger.v('今日头条全民抽奖增加次数失败:没有可以完成的任务')
    else:
        Logger.e('今日头条全民抽奖增加次数失败', '未获取到任务列表')


def _finishTask(id):
    api = HOST + 'finish-task-callback?TaskNo=' + id + '&Code=0'
    response = get(api, headers=getHeaders(), verify=False)
    if response['Code'] == '0':
        return True
    else:
        Logger.e('今日头条全民抽奖完成任务' + id + '失败:', response['Msg'])
        return False


if __name__ == "__main__":
    autoLottery()
