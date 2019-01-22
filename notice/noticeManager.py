# -*-encoding: utf-8 -*-
#统一的通知发送中心

from config import getGeneralConfig
from users import MANAGER
import notice.sendSMS 
import notice.sendMail 
import notice.sendWechat 
from logger import Logger

noticeWays = getGeneralConfig()['notice_ways']

def sendNotice(text,toUser = MANAGER):
    result = []
    if 'sms' in noticeWays:
        if not toUser.Phone is None:
           if len(text)>12:
              text = text[:12]
              Logger.v('短信<'+text+'>长度超过限制,已自动截取前12个字符')
           notice.sendSMS.sendTemplateSMS(toUser.Phone,text)
           result.append('发送短信成功')
    if 'email' in noticeWays:
        if not toUser.Email is None:
           notice.sendMail.sendText(toUser.Email,text)
           result.append('发送邮件成功')
    if 'wechat' in noticeWays:
        if not toUser.Id is None:
           notice.sendWechat.sendTextMsg(toUser.Id,text)
           result.append('发送微信成功')
    Logger.v('发送通知--->'+'<'+text+'>至<'+toUser.Name+'>,结果<'+','.join(result)+'>')
