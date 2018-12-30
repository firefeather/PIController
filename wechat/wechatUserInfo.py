# -*- coding: utf-8 -*-
# 微信用户信息

from wechat.tocken import Tocken
from fetch import get,post

def getWechatUser(openId):
    accessToken = Tocken().get_access_token()
    postUrl = ("https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN" % (accessToken , openId))
    result = get(postUrl)
    return result
  
if __name__ == '__main__':
    getWechatUser('omyqB1uI5qSm5Ypdum43V2zMrTVk')
    getWechatUser('gh_c641cba4b719')

    