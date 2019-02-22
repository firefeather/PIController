# -*- coding: utf-8 -*-
# 主入口

import web
from wechat.handle import Handle
from notice.sendWechat import sendTextMsg
from users import MANAGER
import task
from logger import Logger
from utils.speaker import speak

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    try:
        noticeTxt = '树莓派控制器已启动'
        speak(noticeTxt)
        sendTextMsg(MANAGER.Id,noticeTxt)
        task.startTasks()
        app = web.application(urls, globals())
        app.run()
    except Exception as e:
        Logger.n('控制器启动失败',e)
