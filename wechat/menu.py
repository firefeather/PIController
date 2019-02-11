# -*- coding: utf-8 -*-
# filename: menu.py
# 公众号菜单(需提前单独执行)

import sys
sys.path.append("../")
from tocken import Tocken
from fetch import get,post

class Menu(object):
    def __init__(self):
        pass
    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        if isinstance(postData, str):
            postData = postData.encode('utf-8')
        result = post(postUrl,postData)
        print ('create:',result)

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        result = get(postUrl)
        print ('query:',result)

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        result = get(postUrl)
        print ('delete:',result)

    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        result = get(postUrl)
        print ('get_current_selfmenu_info:',result)

if __name__ == '__main__':
    myMenu = Menu()
    data = """
    {
        "button":
        [
            {
                "name": "快捷命令",
                "sub_button":
                [
                    {
                        "type": "click",
                        "name": "日志",
                        "key":  "log"
                    },
                    {
                        "type": "click",
                        "name": "截屏",
                        "key":  "screen"
                    },
                    {
                        "type": "click",
                        "name": "任务",
                        "key":  "task"
                    },
                    {
                        "type": "click",
                        "name": "重启",
                        "key":  "restart"
                    }
                ]
            },
            {
                "type": "click",
                "name": "命令帮助",
                "key":  "help"
            },
        ],
    }
    """
    accessToken = Tocken().get_access_token()
    #myMenu.delete(accessToken)
    myMenu.create(data, accessToken)