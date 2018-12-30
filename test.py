# -*- coding: utf-8 -*-
# 主入口

import web
import controllers.controller as controllers
from users import MANAGER

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
#    text = input('请输入命令\n')
#    result = controllers.handImage("http://yun.itheima.com/Upload/Images/20170614/594106ee6ace5.jpg",MANAGER)
   result = controllers.handText("设置机器人:图灵",MANAGER)
   print('result:',result)
   result = controllers.handText("你好",MANAGER)
   print('result:',result)
