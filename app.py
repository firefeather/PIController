# -*- coding: utf-8 -*-
# 主入口

import web
from wechat.handle import Handle
from notice.sendWechat import sendTextMsg
from users import MANAGER
import task
from logger import Logger

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    try:
        sendTextMsg(MANAGER.Id,'树莓派控制器已启动')
        task.startTasks()
        app = web.application(urls, globals())
        app.run()
    except Exception as e:
        Logger.n('控制器启动失败',e)
