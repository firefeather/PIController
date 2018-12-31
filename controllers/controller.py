# -*- coding: utf-8 -*-
# 主控制器,所有的命令经由这里分发

import time
from allComands import findComandByStr
from controllers.executor import executCommand
from tools.chatBot import getCurrentChatBot,getReply,getPictureReplyByXiaoBing

def handText(text,user):
   # print('命令:',text,'发起人:',user)
   command = findComandByStr(text.strip())
   if command is None:
       if getCurrentChatBot() is None:
          result = '未找到命令:<'+text+'>'
       else:
          result = getReply(text)
   elif isinstance(command, str):
       result = '<'+text+'>'+command
   else:
       print('找到命令:',command)
       if command.Permission > user.Level:
          result = '<'+text+'>:权限不足'
       else:
          result = '<'+text+'>\n'+executCommand(command,user)
   return result

def handImage(imageUrl,user):
    print('命令:',imageUrl,'发起人:',user)
   #  if not getCurrentChatBot() is None:
         #  result = getPictureReplyByXiaoBing(imageUrl)
    result = getPictureReplyByXiaoBing(imageUrl)
    return result