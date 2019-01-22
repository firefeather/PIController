# -*- coding: utf-8 -*-
# 主入口

import web
from wechat.handle import Handle
from notice.sendWechat import sendTextMsg
from users import MANAGER
import task

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    sendTextMsg(MANAGER.Id,'树莓派小助手已启动')
    task.startTasks()
    app = web.application(urls, globals())
    app.run()
