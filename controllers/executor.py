# -*- coding: utf-8 -*-
# 主控制器,所有的命令经由这里分发

import time, threading, shutil, subprocess, os
from users import getUsers, updateUserByDict, findUser
from wechat.wechatUserInfo import getWechatUser
from allComands import ALL_COMANDS
from notice.noticeManager import sendNotice
from tools.ip import getServerIp
from spider.movies import getMovies
from spider.news import getNews
from script.screenShoot import getScreenImg
from notice.sendWechat import sendImageMsg, sendTextMsg
from tools.translate import translate
from tools.weather import getWeather
from tools.chatBot import setChatBot, clearChatBot
from spider.lagou import getJobInfo
from utils.excel2Image import ReportImage
from tools.weiBoSender import sendWeibo
from logger import Logger
from task import getJobs


def executCommand(command, user):
    if command.Name == ALL_COMANDS[0].Name:  #获取所有用户
        users = getUsers()
        result = '当前共{}位用户:\n'.format(len(users))
        for temp in users:
            result += (
                temp.Name + '(' + temp.Id + '):' + '%s' + '\n') % temp.Level
    elif command.Name == ALL_COMANDS[1].Name:  #获取用户微信信息
        if 'id' in command.Parmas:
            userId = command.Parmas['id']
            result = sendResultLater(user, _getWechatUserInfoAndSend, (userId))
        else:
            result = '未指定id无法查询'
    elif command.Name == ALL_COMANDS[2].Name:  #更新用户信息
        if 'id' in command.Parmas:
            targetUserId = command.Parmas['id']
            users = findUser(id=targetUserId)
            if len(users) == 0:
                result = '未找到指定用户,更新失败'
            else:
                targetUser = users[0]
                if user.Level <= targetUser.Level:
                    result = '权限不足,无法修改'
                else:
                    result = updateUserByDict(command.Parmas)
        else:
            result = '未指定id无法更新'
    elif command.Name == ALL_COMANDS[3].Name:  #获取IP地址
        result = sendResultLater(user, getServerIp)
    elif command.Name == ALL_COMANDS[4].Name:  #获取最新电影
        result = sendResultLater(user, getMovies)
    elif command.Name == ALL_COMANDS[5].Name:  #截屏
        result = sendResultLater(user, getScreenImg)
    elif command.Name == ALL_COMANDS[6].Name:  #新闻
        result = sendResultLater(user, getNews)
    elif command.Name == ALL_COMANDS[7].Name:  #翻译
        result = translate(command.Parmas)
    elif command.Name == ALL_COMANDS[8].Name:  #天气
        result = getWeather(command.Parmas)
    elif command.Name == ALL_COMANDS[9].Name:  #设置机器人
        result = setChatBot(command.Parmas)
    elif command.Name == ALL_COMANDS[10].Name:  #取消机器人
        clearChatBot()
        result = '已取消聊天机器人'
    elif command.Name == ALL_COMANDS[11].Name:  #拉勾职位
        threading.Thread(
            target=_getJobInfoAndSend, args=(user, command.Parmas)).start()
        result = '已开始查询'
    elif command.Name == ALL_COMANDS[12].Name:  #群发消息
        threading.Thread(
            target=_sendMsgToAll, args=(user, command.Parmas)).start()
        result = '已开始发送'
    elif command.Name == ALL_COMANDS[13].Name:  #执行shell命令
        threading.Thread(
            target=_executeShell, args=(user, command.Parmas)).start()
        result = '已开始执行<' + command.Parmas + '>'
    elif command.Name == ALL_COMANDS[14].Name:  #发微博
        result = sendResultLater(user, sendWeibo, command.Parmas)
    elif command.Name == ALL_COMANDS[15].Name:  #获取定时任务情况
        result = getJobs()
    else:
        result = '暂未完成'
    Logger.v(user.Name + '的命令<' + command.Name + '>执行结果<' + result + '>')
    return result


def sendResultLater(to, func, args=None):
    def getResultAndSend():
        try:
            result = func() if args is None else func(args)
            if len(result) < 50 and ('.png' in result
                                     or '.jpg' in result):  #如果是个图片 则发送图片
                sendImageMsg(to.Id, result)
                os.remove(result)
            else:
                sendTextMsg(to.Id, result)
        except Exception as e:
            Logger.e(func.__name__+'执行失败', e)
        #  print(func,' error',e)
    threading.Thread(target=getResultAndSend).start()
    return '已开始执行'


def _getJobInfoAndSend(to, jobName):
    try:
        filePath = getJobInfo(jobName)
        tempDir = 'temp/'
        images = ReportImage.excel2Image(filePath, tempDir, 50)
        for image in images:
            sendImageMsg(to.Id, image)
        shutil.rmtree(tempDir)
    except Exception as e:
        Logger.e('爬取拉勾数据失败', e)


def _getWechatUserInfoAndSend(userId):
    userInfo = getWechatUser(userId)
    if 'errcode' in userInfo:
        result = userInfo['errmsg']
        Logger.e('从微信获取用户信息失败', result)
    else:
        updateUserByDict(userInfo)
        result = '姓名:'+userInfo['nickname']+'\n'+\
                 '性别:'+('男' if userInfo['sex'] == 1 else '女')+'\n'+\
                 '省份:'+userInfo['province']+'\n'+\
                 '城市:'+userInfo['city']+'\n'+\
                 '头像:'+userInfo['headimgurl']+'\n'+\
                 '时间:'+time.strftime("%Y年%m月%d日",time.localtime(userInfo['subscribe_time']))+'\n'
    return result


def _sendMsgToAll(commander, msg):
    users = getUsers()
    result = ''
    if len(users) > 0:
        for user in users:
            sendTextMsg(user.Id, msg)
        result = '已发送<' + msg + '>至{}位用户'.format(len(users))
    else:
        result = '没有可用用户'
    sendTextMsg(commander.Id, result)


def _executeShell(user, command):
    status, output = subprocess.getstatusoutput(command)
    result = ('执行成功:\n' if status == 0 else '执行失败:\n') + output
    sendTextMsg(user.Id, result)
