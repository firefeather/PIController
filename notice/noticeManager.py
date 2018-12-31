# -*-encoding: utf-8 -*-
#统一的通知发送中心

from config import getGeneralConfig
from users import MANAGER
from notice.sendSMS import sendTemplateSMS
from notice.sendMail import sendText
from notice.sendWechat import sendTextMsg

noticeWays = getGeneralConfig()['notice_ways']

def sendNotice(text,toUser = MANAGER):
    result = []
    if 'sms' in noticeWays:
        if not toUser.Phone is None:
           sendTemplateSMS(toUser.Phone,text)
           result.append('发送短信成功')
    if 'email' in noticeWays:
        if not toUser.Email is None:
           sendText(toUser.Email,text)
           result.append('发送邮件成功')
    if 'wechat' in noticeWays:
        if not toUser.Id is None:
           sendTextMsg(toUser.Id,text)
           result.append('发送微信成功')
    print(text,toUser,"发送结果:",result)