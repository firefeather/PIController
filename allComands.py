# -*- coding: utf-8 -*-
# 所有的命令

import copy
from command import Command,PERMISSION_LEVEL
from tools.chatBot import BOTS

global ALL_COMANDS
ALL_COMANDS = [
   Command(name='获取所有用户',func='获取当前系统所有的用户信息',usage='获取所有用户',parmas=None,permission=PERMISSION_LEVEL['SUPER']),
   Command(name='获取用户信息',func='传入用户id,获取指定用户的微信信息',usage='获取用户信息:id=XXX',parmas="DIC",permission=PERMISSION_LEVEL['ADMIN']),
   Command(name='更新用户',func='更新用户(包含姓名、权限、电话、邮箱等),必须包含id参数,其他可选',usage='更新用户:id=XXX,level=XXX,name=XXX',parmas="DIC",permission=PERMISSION_LEVEL['ADMIN']),
   Command(name='获取ip',func='获取服务器的IP地址',usage='获取ip',parmas=None,permission=PERMISSION_LEVEL['ADMIN']),
   Command(name='最新电影',func='获取猫眼上最新电影前十名',usage='最新电影',parmas=None,permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='截屏',func='获取服务器当前屏幕截图',usage='截屏',parmas=None,permission=PERMISSION_LEVEL['SUPER']),
   Command(name='新闻',func='获取feebuf最新安全新闻',usage='新闻',parmas=None,permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='翻译',func='获取有道翻译结果',usage='翻译:XXX',parmas='STR',permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='查询天气',func='获取指定地区(最小为区县)的当日天气情况',usage='查询天气:XXX',parmas='STR',permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='设置机器人',func='设置聊天机器人,当前支持'+','.join(BOTS)+',如参数错误则随机机器人',usage='设置机器人:XXX',parmas='STR',permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='取消机器人',func='取消聊天机器人',usage='取消机器人',parmas=None,permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='职位信息',func='获取指定岗位在拉勾上的最新信息',usage='职位信息:XXX',parmas='STR',permission=PERMISSION_LEVEL['NORMAL']),
   Command(name='群发消息',func='群发消息给所有用户',usage='群发消息:XXX',parmas='STR',permission=PERMISSION_LEVEL['SUPER']),
   Command(name='执行代码',func='在命令终端中执行相应的代码',usage='执行代码:XXX',parmas='STR',permission=PERMISSION_LEVEL['SUPER']),
   Command(name='发微博',func='模拟网页登录发送微博(会带小尾巴)',usage='发微博:XXX',parmas='STR',permission=PERMISSION_LEVEL['SUPER']),

]

def findComandByStr(text):#根据用户输入尝试解析出对应命令
    args = text.split(":")  # 参数以:为分割符
    comandName = args[0].strip()#命令名
    global ALL_COMANDS
    commandList = list(filter(lambda com:com.Name == comandName, ALL_COMANDS))
    result = None

    if len(commandList) != 0:#找到了该命令
       comand = copy.deepcopy(commandList[0])
       if comand.Parmas == None:
          result = comand
       elif comand.Parmas == "STR":
          if len(args) > 1:#有参数命令,需解码参数
             comand.Parmas = args[1].strip()
             result = comand
       elif comand.Parmas == "DIC":
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
               except Exception:
                  print('命令参数解析失败')
       else:
          result = comand
       if result is None:
          result = '参数错误,用法:\n'+comand.Usage
       return result
    else:
        print('未找到指定命令')
        return None



if __name__ == "__main__":
    comand = findComandByStr('a:(abc123,bcd456)')
    if comand is None:
       print('未找到命令')
    elif isinstance(comand, str):
       print('参数错误:',comand)
    else:
       print('找到命令:',comand)


       