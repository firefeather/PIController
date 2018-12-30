# -*- coding: utf-8 -*-
# 主入口

import web
from wechat.handle import Handle

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()