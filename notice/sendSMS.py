# coding:utf-8
#通过腾讯云发送短信  100条/月
from qcloudsms_py import QcloudSms
from config import getSmsConfig
from logger import Logger

smsConfig = getSmsConfig()
qcloudsms = QcloudSms(smsConfig['appid'], smsConfig['appkey'])  

template_id = smsConfig['template_id']
sign = smsConfig['sms_sign']

def sendTemplateSMS(toNumber,text):
    ssender = qcloudsms.SmsSingleSender()
    params = [text]  
    try:
        sendResult = ssender.send_with_param(86, toNumber,
            template_id, params, sign=sign, extend="", ext="")
        if sendResult['result']!=0:
            Logger.e('短信发送失败',sendResult['errmsg'])
            return False
        return True
        # print('短信发送结果:',sendResult)
    except Exception as e:
        Logger.e('发送短信失败', e)
        return False

def sendGroupTemplateSMS(toNumbers,text):
    msender = qcloudsms.SmsMultiSender()
    params = [text]
    try:
        sendResult = msender.send_with_param(86, toNumbers,
            template_id, params, sign, extend="", ext="") 
        print('短信群发结果:',sendResult)
    except Exception as e:
        print('短信发送失败:',e)

