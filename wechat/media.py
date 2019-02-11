# -*- coding: utf-8 -*-
# filename: media.py
# 临时素材上传与下载

import json
from wechat.tocken import Tocken
from fetch import post, download as getFile


def upload(filePath, mediaType):
    accessToken = Tocken().get_access_token()
    file = {'file': open(filePath, 'rb')}
    param = {'media': file}
    postUrl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (
        accessToken, mediaType)
    result = post(postUrl, files=file)
    # print('upload:', filePath, result)
    return result


def download(filePath, mediaId):
    accessToken = Tocken().get_access_token()
    postUrl = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (
        accessToken, mediaId)
    r = getFile(postUrl)
    with open(filePath, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


if __name__ == '__main__':
    upload('../test.png', 'image')
