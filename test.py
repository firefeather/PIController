# -*- coding: utf-8 -*-
# 主入口

import web
import controllers.main as controllers
from users import MANAGER

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
   text = input('请输入命令\n')
   result = controllers.handCommands(text,MANAGER)
   print('result:',result)
