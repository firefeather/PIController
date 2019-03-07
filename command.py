# -*- coding: utf-8 -*-
# 命令

from baseObject import BaseObject

PERMISSION_LEVEL={
  'SUPER':9,#超级管理员
  'ADMIN':8,#管理员
  'NORMAL':0,#一般用户
  'BLACK':-1#黑名单用户
}

class Command(BaseObject):
      def __init__(self, **info):
          if 'name' in info:#命令名
             self.Name = info['name']
          if 'func' in info:#命令作用
             self.Func = info['func']
          if 'usage' in info:#命令用法
             self.Usage = info['usage']
          if 'parmas' in info:#命令参数,None 无参数  STR 字符串参数  DIC 字典类参数 含有NONE字段的为参数可空
             self.Parmas = info['parmas']
          if 'default' in info:#默认参数
             self.Default = info['default']
          else:
             self.Default = None
          if 'permission' in info:#命令所需权限等级
             self.Permission = info['permission']
          else:
             self.Permission = PERMISSION_LEVEL['NORMAL']
