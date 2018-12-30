# -*- coding: utf-8 -*-
# 用户

import time
from baseObject import BaseObject
from wechat.wechatUserInfo import getWechatUser

class User(BaseObject):
    def __init__(self, **info):
        if 'id' in info:
           self.Id = info['id']
        else:
           raise RuntimeError("用户id为空无法添加")
        nowTime = int(time.time())
        if 'name' in info:
           self.Name = info['name']
        else:
           self.Name = '未命名{}'.format(nowTime)
        if 'level' in info:
           self.Level = info['level']
        else:
           self.Level = 0
        if 'phone' in info:
           self.Phone = info['phone']
        if 'email' in info:
           self.Email = info['email']
        self.Time = nowTime
    

