# -*- coding: utf-8 -*-
# 所有的命令

import copy,time
from command import Command,PERMISSION_LEVEL
from tools.chatBot import BOTS
from logger import Logger

global ALL_COMANDS
ALL_COMANDS = [
   Command(name='所有用户',func='获取当前系统所有的用户信息',usage='所有用户',parmas=None,permission=PERMISSION_LEVEL['SUPER']),
   Command(name='用户信息',func='传入用户id,获取指定用户的微信信息',usage='用户信息:id=XXX',parmas="DIC",permission=PERMISSION_LEVEL['ADMIN']),
   Command(name='更新用户',func='更新用户(包含姓名、权限、电话、邮箱等),必须包含id参数,其他可选',usage='更新用户:id=XXX,level=XXX,name=XXX',parmas="DIC",permission=PERMISSION_LEVEL['ADMIN']),
   Command(name='获取ip',func='获取服务器的IP地址',usage='获取ip',parmas=None,permission=PERMISSION_LEVEL['ADMIN']),
   Command(name='电影',func='获取猫眼上最新电影前十名',usage='电影',parmas=None,permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='截屏',func='获取服务器当前屏幕截图',usage='截屏',parmas=None,permission=PERMISSION_LEVEL['SUPER']),
   Command(name='新闻',func='获取feebuf最新安全新闻',usage='新闻',parmas=None,permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='翻译',func='获取有道翻译结果',usage='翻译:XXX',parmas='STR',permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='天气',func='获取指定地区(最小为区县)的当日天气情况',usage='天气:XXX',parmas='STR',permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='设置机器人',func='设置聊天机器人,当前支持'+','.join(BOTS)+',如参数错误则随机机器人',usage='设置机器人:XXX',parmas='STR',permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='取消机器人',func='取消聊天机器人',usage='取消机器人',parmas=None,permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='职位信息',func='获取指定岗位在拉勾上的最新信息',usage='职位信息:XXX',parmas='STR',permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='群发消息',func='群发消息给所有用户',usage='群发消息:XXX',parmas='STR',permission=PERMISSION_LEVEL['SUPER']),
   Command(name='执行代码',func='在命令终端中执行相应的代码',usage='执行代码:XXX',parmas='STR',permission=PERMISSION_LEVEL['SUPER']),
   Command(name='发微博',func='模拟网页登录发送微博(会带小尾巴)',usage='发微博:XXX',parmas='STR',permission=PERMISSION_LEVEL['SUPER']),
   Command(name='任务详情',func='获取定时任务的详细情况',usage='任务详情',parmas=None,permission=PERMISSION_LEVEL['SUPER']),
   Command(name='执行任务',func='立即执行指定的定时任务',usage='执行任务:name=xxx',parmas='DIC',permission=PERMISSION_LEVEL['SUPER']),
   Command(name='说话',func='让树莓派通过音响将指定文字说出来',usage='说话:XXX',parmas='STR',permission=PERMISSION_LEVEL['ADMIN']),
   Command(name='查看日志',func='查看指定日期日志文件(格式YYYY-MM-DD)',usage='查看日志:X-X-X',parmas='STR/NONE',permission=PERMISSION_LEVEL['SUPER']),
   Command(name='重启系统',func='拉取最新代码并重启控制器',usage='重启系统',parmas=None,permission=PERMISSION_LEVEL['SUPER']),
   Command(name='小米众筹',func='获取小米优品上最新的众筹产品信息',usage='小米众筹',parmas=None,permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='设备信息',func='获取当前服务器的状态信息',usage='设备信息',parmas=None,permission=PERMISSION_LEVEL['ADMIN']),
   Command(name='双色球',func='获取指定期数双色球开奖号码',usage='双色球:XXX',parmas='STR/NONE',permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='帮助',func='获取命令帮助及用法',usage='帮助',parmas=None,permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='小爱同学',func='让树莓派呼叫小爱同学并对其说话',usage='小爱同学:XXX',parmas='STR',permission=PERMISSION_LEVEL['ADMIN']),
   Command(name='发微信',func='给指定人发送文字微信',usage='发微信:to=XXX,text=XXX',parmas='DIC',permission=PERMISSION_LEVEL['ADMIN']),
   Command(name='微信电话',func='给指定人发送微信视频电话',usage='微信电话:XXX',parmas='STR/NONE',permission=PERMISSION_LEVEL['ADMIN']),

]

def findComandByStr(text):#根据用户输入尝试解析出对应命令
    args = text.split(":",1)  # 参数以:为分割符
    if len(args) == 1:
       args = text.split("：",1)  # 再尝试参数以：为分割符
    comandName = args[0].strip()#命令名
    global ALL_COMANDS
    commandList = list(filter(lambda com:com.Name == comandName, ALL_COMANDS))
    result = None
    if len(commandList) != 0:#找到了该命令
       comand = copy.deepcopy(commandList[0])
       if comand.Parmas == None:
          result = comand
       elif "STR" in comand.Parmas:#字符串型参数
          if len(args) > 1:#有参数命令,需解码参数
             comand.Parmas = args[1].strip()
             result = comand
          elif not comand.Default is None:
             comand.Parmas = comand.Default
             result = comand
       elif "DIC" in comand.Parmas:#字典型参数
            if len(args) > 1:#有参数命令,需解码参数
               try:
                  parmasList = args[1].split(",")
                  data={}
                  for parma in parmasList:
                     keyValue = parma.split("=")
                     key = keyValue[0].strip() 
                     value = keyValue[1].strip() 
                     data[key]=value
                  comand.Parmas = data
                  result = comand
               except Exception as e:
                  Logger.e('命令参数解析失败', e)
            elif not comand.Default is None:
               comand.Parmas = comand.Default
               result = comand
       else:
          result = comand
       if result is None:
          if "NONE" in comand.Parmas:
             comand.Parmas = None
             result = comand
          else:
             result = '参数错误,用法:\n'+comand.Usage
       return result
    else:
      #   print('未找到指定命令')
        return None



if __name__ == "__main__":
    comand = findComandByStr('a:(abc123,bcd456)')
    if comand is None:
       print('未找到命令')
    elif isinstance(comand, str):
       print('参数错误:',comand)
    else:
       print('找到命令:',comand)


       