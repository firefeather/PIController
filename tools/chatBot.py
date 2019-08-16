import requests, time, random, re, base64, os, json,string
from urllib.parse import quote,urlencode
from logger import Logger
import hashlib

BOTS = ['图灵', '小冰', '小I','腾讯']

global _CURRENT_BOT
_CURRENT_BOT = BOTS[3]


def setChatBot(bot):
    global _CURRENT_BOT
    _CURRENT_BOT = bot
    if _CURRENT_BOT not in BOTS:
        _CURRENT_BOT = random.choice(BOTS)
    return '已成功设置当前聊天机器人为:' + _CURRENT_BOT


def clearChatBot():
    global _CURRENT_BOT
    _CURRENT_BOT = None


def getCurrentChatBot():
    global _CURRENT_BOT
    return _CURRENT_BOT


def formatTulingNews(newsList):
    newsTxt = '\n'
    for news in newsList:
        newsTxt += news.get('article') + '\n' + news.get('detailurl') + '\n\n'
    return newsTxt


def getTulingResponse(msg):
    Url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': '75137612d89c42f0b9d7a3f5133ec656',  #这个key可以直接拿来用，随便用，无所谓，放心公开
        'info': msg,
        'userid': 'pth-robot',
    }
    try:
        r = requests.post(Url, data=data).json()
        text = r.get('text')
        uri = r.get('url')
        news = r.get('list')
        if uri:
            text += (':\n' + uri)
        if news:
            text += (':\n' + formatTulingNews(news))
        return text
    except:
        return


def getXiaoIResponse(msg):
    ini = "{'sessionId':'09e2aca4d0a541f88eecc77c03a8b393','robotId':'webbot','userId':'462d49d3742745bb98f7538c42f9f874','body':{'content':'" + msg + "'},'type':'txt'}&ts=1529917589648"
    url = "http://i.xiaoi.com/robot/webrobot?&callback=__webrobot_processMsg&data=" + quote(
        ini)
    cookie = {
        "cnonce": "808116",
        "sig": "0c3021aa5552fe597bb55448b40ad2a90d2dead5",
        "XISESSIONID": "hlbnd1oiwar01dfje825gavcn",
        "nonce": "273765",
        "hibext_instdsigdip2": "1"
    }
    r = requests.get(url, cookies=cookie)
    pattern = re.compile(r'\"fontColor\":0,\"content\":\"(.*?)\"')
    result = pattern.findall(r.text)
    return random.choice(result).strip(r'\n\r\n')

def ranstr(num=16):
    rule = string.ascii_lowercase + string.digits
    str = random.sample(rule, num)
    return "".join(str)

global tencent_session
tencent_session='89898'

def getTencentSign(para, app_key='yUqMILgIFnDAFymX'):
    # 签名的key有严格要求，按照key升序排列
    data = sorted(para.items(), key=lambda item: item[0])
    data.append(('app_key',app_key))
    s = urlencode(data)
    # 计算md5报文信息
    md5 = hashlib.md5()
    md5.update(s.encode())
    digest = md5.hexdigest()
    return digest.upper()

def getTencentResponse(msg):
    try:
        global tencent_session
        api = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'
        params = {
            'app_id':'2120411915',
            'time_stamp':str(int(time.time())),
            'nonce_str':ranstr(),
            'session':tencent_session,
            'question':msg.encode('gbk'),
        }
        params['sign']=getTencentSign(params)
        res = requests.post(api, data=params).json()
        result = ''
        if res['ret'] == 0:
            data = res['data']
            result = data['answer']
            tencent_session = data['session']
        else:
            result = res['msg']
        return result
    except Exception as e:
        Logger.e('获取腾讯智能闲聊结果失败', e)
        return 'Emmmmm'
# def getXiaoBingResponse(msg):


# 微信好友发来的内容isFriendChat=True, 群聊发来的内容isGroupChat=True, 公众号发来的内容isMpChat=False
def getReply(msg):
    global _CURRENT_BOT
    # 发送图灵机器人回复内容
    if _CURRENT_BOT == BOTS[0]:
        reply = getTulingResponse(msg)
    # 发送小冰回复内容
    elif _CURRENT_BOT == BOTS[1]:
        reply = '小冰不在,图灵代回:' + getTulingResponse(msg)
    # 发送小I回复内容
    elif _CURRENT_BOT == BOTS[2]:
        reply = getXiaoIResponse(msg)
    # 发送腾讯回复内容
    elif _CURRENT_BOT == BOTS[2]:
        reply = getTencentResponse(msg)
    else:
        reply = '请先设置聊天机器人'
    return reply or 'I received: ' + msg


def getPictureReplyByXiaoBing(url):
    try:
        imgData = requests.get(url).content
        # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
        # with open( './a.jpg','wb' ) as f:
        #      f.write(img)
        header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
            'Referer':
            'http://kan.msxiaobing.com/V3/Portal',
        }
        url1 = 'http://kan.msxiaobing.com/Api/Image/UploadBase64'
        url2 = 'https://kan.msxiaobing.com/Api/ImageAnalyze/Process'
        s = requests.Session()
        imgData = base64.b64encode(imgData)
        r = s.post(url1, data=imgData, headers=header)
        imgurl = 'https://mediaplatform.msxiaobing.com' + r.json()['Url']
        sys_time = int(time.time())
        payload = {
            'service': 'yanzhi',
            'tid': '7531216b61b14d208496ee52bca9a9a8'
        }
        headerss = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
            'Cookie':
            '_ga=GA1.2.1597838376.1504599720; _gid=GA1.2.1466467655.1504599720; ai_user=sp1jt|2017-09-05T10:53:04.090Z; cpid=YDLcMF5LPDFfSlQyfUkvMs9IbjQZMiQ2XTJHMVswUTFPAA; salt=EAA803807C2E9ECD7D786D3FA9516786; ARRAffinity=3dc0ec2b3434a920266e7d4652ca9f67c3f662b5a675f83cf7467278ef043663; ai_session=sQna0|1504664570638.64|1504664570638'
            + str(random.randint(11, 999)),
            'Referer':
            'https://kan.msxiaobing.com/ImageGame/Portal?task=yanzhi&feid=d89e6ce730dab7a2410c6dad803b5986'
        }
        form = {
            'MsgId': str(sys_time) + '733',
            'CreateTime': sys_time,
            'content[imageUrl]': imgurl
        }
        r = requests.post(url2, params=payload, data=form, headers=headerss)
        text1 = r.json()['content']['text']
        return text1
    except Exception as e:
        Logger.e('图片分析失败', e)
        return 'Emmmmm'
        # print('图片分析失败:',e)

if __name__ == '__main__':
    print(getTencentResponse('你好'))