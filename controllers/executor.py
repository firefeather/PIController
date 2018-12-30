# -*- coding: utf-8 -*-
# 主控制器,所有的命令经由这里分发

import time
from users import getUsers,updateUserByDict,findUser
from wechat.wechatUserInfo import getWechatUser
from allComands import ALL_COMANDS
from notice.noticeManager import sendNotice
from tools.ip import getServerIp
from spider.movies import getMovies
from spider.news import getNews
from script.screenShoot import getScreenImg
from notice.sendWechat import sendImageMsg
from tools.translate import translate
from tools.weather import getWeather
from tools.chatBot import setChatBot,clearChatBot

def executCommand(command,user):
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
   elif command.Name == ALL_COMANDS[3].Name:#获取IP地址
        result = getServerIp()
   elif command.Name == ALL_COMANDS[4].Name:#获取最新电影
        result = getMovies()
   elif command.Name == ALL_COMANDS[5].Name:#截屏
        result = getScreenImg()
        if '.png' in result:
           sendImageMsg(user.Id,result)
           result = '截图成功'
   elif command.Name == ALL_COMANDS[6].Name:#新闻
        result = getNews()
   elif command.Name == ALL_COMANDS[7].Name:#翻译
        result = translate(command.Parmas)
   elif command.Name == ALL_COMANDS[8].Name:#天气
        result = getWeather(command.Parmas)
   elif command.Name == ALL_COMANDS[9].Name:#设置机器人
        result = setChatBot(command.Parmas)
   elif command.Name == ALL_COMANDS[10].Name:#取消机器人
        clearChatBot()
        result = '已取消聊天机器人'
   else:
        result = '暂未完成'
   return result
