# -*- coding: utf-8 -*-
# 消息处理

import hashlib,web
from wechat import receive,reply
import controllers.controller as controllers
from users import findAndCreatedIfUserNotFound
from allComands import ALL_COMANDS

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, welcome!"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "quaner" 
            list = [token, timestamp, nonce]
            list.sort()
            temp = ''.join(list)
            sha1 = hashlib.sha1(temp.encode('utf-8'))
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument
    def POST(self):
        try:
            webData = web.data()
            recMsg = receive.parse_xml(webData)
            toUserName = recMsg.FromUserName
            fromUserName = recMsg.ToUserName
            fromUser = findAndCreatedIfUserNotFound(id=toUserName)[0]
            if isinstance(recMsg, receive.Msg):
                if recMsg.MsgType == 'text':
                    content = recMsg.Content.decode('utf-8')
                    result = controllers.handText(content,fromUser)
                    replyMsg = reply.TextMsg(toUserName, fromUserName, content+':\n'+result)
                elif recMsg.MsgType == 'image':
                    result = controllers.handImage(recMsg.PicUrl,fromUser)
                    if result is None:
                       replyMsg = reply.ImageMsg(toUserName, fromUserName, recMsg.MediaId)
                    else:
                       replyMsg = reply.TextMsg(toUserName, fromUserName, result)
                else:
                    content = "好的,朕知道了!"
                    replyMsg = reply.TextMsg(toUserName, fromUserName, content)
                return replyMsg.send()
            elif isinstance(recMsg, receive.EventMsg):
                if recMsg.Event == 'CLICK':
                    if recMsg.Eventkey == 'help':
                        commandList = list(filter(lambda com:com.Permission <= fromUser.Level, ALL_COMANDS))
                        if len(commandList) == 0:
                           content = '暂无'
                        else:
                            descs = []
                            for comand in commandList:
                                desc = '命令:'+comand.Name+'\n'+\
                                        '作用:'+comand.Func+'\n'+\
                                        '用法:'+comand.Usage+'\n'
                                descs.append(desc)
                            content = '\n\n'.join(descs)
                elif recMsg.Event in ('subscribe', 'unsubscribe'):
                    if recMsg.Subscribed:
                        content = ("感谢小可爱的关注")
                    else:
                        content = "再见了,小可爱!"
                else:
                    content = "未识别的操作"
                replyMsg = reply.TextMsg(toUserName, fromUserName, content)
                return replyMsg.send()
            else :
                print ("暂且不处理")
                return reply.Msg().send()
        except Exception as Argment:
            return Argment
