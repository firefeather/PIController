# -*-encoding: utf-8 -*-
#统一的通知发送中心

from config import getGeneralConfig
from users import MANAGER
import notice.sendSMS 
import notice.sendMail 
import notice.sendWechat 
from logger import Logger
import platform

noticeWays = getGeneralConfig()['notice_ways']

def sendNotice(text,toUser = MANAGER):
    if platform.system() == 'Darwin':
       _notify('系统通知',text)
    result = []
    if 'sms' in noticeWays:
        if not toUser.Phone is None:
           smsTxt = text
           if len(smsTxt)>12:
              smsTxt = smsTxt[:12]
              Logger.v('短信<'+text+'>长度超过限制,已自动截取前12个字符')
           result.append('发送短信:'+('成功' if notice.sendSMS.sendTemplateSMS(toUser.Phone,smsTxt) else '失败'))
    if 'email' in noticeWays:
        if not toUser.Email is None:
           notice.sendMail.sendText(toUser.Email,text)
           result.append('发送邮件成功')
    if 'wechat' in noticeWays:
        if not toUser.Id is None:
           result.append('发送微信:'+('成功' if notice.sendWechat.sendTextMsg(toUser.Id,text) else '失败'))
    Logger.v('发送通知--->'+'<'+text+'>至<'+toUser.Name+'>,结果<'+','.join(result)+'>')

def sendNoticeAnyway(text,toUser = MANAGER):
    result = False
    if not toUser.Id is None:
       result =  notice.sendWechat.sendTextMsg(toUser.Id,text)
    if not result:
       if not toUser.Email is None:
           result =  notice.sendMail.sendText(toUser.Email,text)
    if not result:
        if not toUser.Phone is None:
           smsTxt = text
           if len(smsTxt)>12:
              smsTxt = smsTxt[:12]
              Logger.v('短信<'+text+'>长度超过限制,已自动截取前12个字符')
           result.append('发送短信:'+('成功' if notice.sendSMS.sendTemplateSMS(toUser.Phone,smsTxt) else '失败'))
    Logger.v('发送通知--->'+'<'+text+'>至<'+toUser.Name+'>,结果:'+('成功' if result else '失败'))

# Mac脚本通知
def _notify(title, text):
   import os
   os.system("""
					osascript -e 'display notification "{0}" with title "{1}"'
				""".format(text, title))