# -*- coding: utf-8 -*-
# 主控制器,所有的命令经由这里分发 做执行前的判断和拦截(用法及权限判断)

import time
from allComands import findComandByStr
from controllers.executor import executCommand
from tools.chatBot import getCurrentChatBot, getReply, getPictureReplyByXiaoBing
from logger import Logger


def handText(text, user,isVoice=False):
    # print('命令:',text,'发起人:',user)
    if not isVoice:
        Logger.v('收到<' + user.Name + '>的文本消息<' + text + '>')
    if text.endswith('。') and text.find('，')<6:#尝试处理下语音消息
          text = text.replace('，',':',1)
          text=text[:-1]
    command = findComandByStr(text.strip())
    if command is None:
        if getCurrentChatBot() is None:
            result = '未找到命令:<' + text + '>'
        else:
            result = getReply(text)
    elif isinstance(command, str):
        result = '<' + text + '>' + command
    else:
        #  print('找到命令:',command)
        Logger.v('执行命令<' + command.Name + '>,参数<' +
                 (str(command.Parmas) or '无') + '>,发起人<' + user.Name + '>')
        if command.Permission > user.Level:
            result = '<' + text + '>:权限不足'
        else:
            result = '<' + text + '>\n' + executCommand(command, user)
    return result


def handImage(imageUrl, user):
    Logger.v('收到<' + user.Name + '>的图片消息<' + imageUrl + '>')
    #  if not getCurrentChatBot() is None:
    #  result = getPictureReplyByXiaoBing(imageUrl)
    result = getPictureReplyByXiaoBing(imageUrl)
    return result

def handVoice(content, user):
    Logger.v('收到<' + user.Name + '>的语音消息<' + content + '>')
    result = handText(content,user,isVoice=True)
    return result