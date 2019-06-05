# -*- coding: utf-8 -*-
# 主入口

import web, os
import controllers.controller as controllers
from users import MANAGER
import task

urls = (
    '/wx',
    'Handle',
)

if __name__ == '__main__':
    # os.system(
    # 			"""
    # 				osascript -e 'display notification "{0}" with title "{1}"'
    # 			""".format('你好啊', '测试下')
    # 		  )
    #    text = input('请输入命令\n')
    #    result = controllers.handImage("http://yun.itheima.com/Upload/Images/20170614/594106ee6ace5.jpg",MANAGER)
       result = controllers.handText("执行任务:name=_addBaiduJob",MANAGER)
    #    result = controllers.handText("小爱同学:明天天气怎么样?",MANAGER)
       print('result:',result)
    #    result = controllers.handText("立即执行任务:name=_clearLog",MANAGER)
    #    result = controllers.handText("获取用户信息:id=omyqB1uI5qSm5Ypdum43V2zMrTVk",MANAGER)
    #    print('result',result)
    # task.startTasks()
    # print(task.getJobs())
