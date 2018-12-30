# -*- coding: utf-8 -*-
# 主控制器,所有的命令经由这里分发

import time
from users import getUsers,updateUserByDict,findUser
from wechat.wechatUserInfo import getWechatUser
from allComands import findComandByStr,ALL_COMANDS

def handCommands(commandText,user):
   # print('命令:',commandText,'发起人:',user)
   command = findComandByStr(commandText.strip())
   if command is None:
       result = '未找到命令'
   elif isinstance(command, str):
       result = command
   else:
       print('找到命令:',command)
       if command.Permission > user.Level:
          result = '权限不足'
       else:
          if command.Name == ALL_COMANDS[0].Name:#获取所有用户
             users = getUsers()
             result = ''
             for temp in users:
                result += (temp.Name+'('+temp.Id+'):'+'%s'+'\n') % temp.Level
          elif command.Name == ALL_COMANDS[1].Name:#获取用户微信信息
             if 'id' in command.Parmas:
                userId = command.Parmas['id']
                userInfo = getWechatUser(userId)
                if 'errcode' in userInfo:
                   print('获取用户信息失败:',userInfo['errmsg'])
                   result = userInfo['errmsg']
                else:
                   updateUserByDict(userInfo)
                   result = '姓名:'+userInfo['nickname']+'\n'+\
                           '性别:'+('男' if userInfo['sex'] == 1 else '女')+'\n'+\
                           '省份:'+userInfo['province']+'\n'+\
                           '城市:'+userInfo['city']+'\n'+\
                           '头像:'+userInfo['headimgurl']+'\n'+\
                           '时间:'+time.strftime("%Y年%m月%d日",time.localtime(userInfo['subscribe_time']))+'\n'
             else:
                result = '未指定id无法查询'
          elif command.Name == ALL_COMANDS[2].Name:#更新用户信息
             if 'id' in userInfo:
                targetUserId = command.Parmas['id']
                targetUser = findUser(id=targetUserId)
                if user.Level<=targetUser.Level:
                   result = '权限不足,无法修改'
                else:
                   result = updateUserByDict(command.Parmas)
             else:
                result = '未指定id无法更新'
          else:
             result = '暂未完成'
   return result
