# coding:utf-8
#通过微信公众号发送微信消息
from wechat.tocken import Tocken
from fetch import get,post
from wechat.media import upload
from logger import Logger

def sendMsg(msgJson):
    accessToken = Tocken().get_access_token()
    postUrl = ("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % accessToken )
    result = post(postUrl,json=msgJson)
    if result['errcode']:
       Logger.e('发送微信消息失败',result['errmsg'])
       return False
    return True

def sendTextMsg(toId,content):
    if content is None or content == '':
       Logger.e('发送微信消息失败',"消息内容为空")
       return False
    msgJson = {
              "touser":toId,
              "msgtype":"text",
              "text":
                  {
                  "content":content.encode("utf-8").decode("latin1")
                  }   
            }
    return sendMsg(msgJson)

def sendImageMsg(toId,path):
    result = upload(path,'image')
    if 'errcode' in result:
       Logger.e('文件上传失败', result['errmsg'])
       return sendTextMsg(toId,'文件上传失败:'+result['errmsg'])
    mediaId = result['media_id']
    msgJson = {
              "touser":toId,
              "msgtype":"image",
              "image":
              {
                "media_id":mediaId
              } 
            }
    return sendMsg(msgJson)
  
def sendVoiceMsg(toId,path):
    result = upload(path,'voice')
    if 'errcode' in result:
       Logger.e('文件上传失败', result['errmsg'])
       return sendTextMsg(toId,'文件上传失败:'+result['errmsg'])
    mediaId = result['media_id']
    msgJson = {
              "touser":toId,
              "msgtype":"voice",
              "voice":
              {
                "media_id":mediaId
              } 
            }
    return sendMsg(msgJson)

def sendVideoMsg(toId,path,title,desc):
    result = upload(path,'video')
    if 'errcode' in result:
       Logger.e('文件上传失败', result['errmsg'])
       return sendTextMsg(toId,'文件上传失败:'+result['errmsg'])
    mediaId = result['media_id']
    msgJson = {
              "touser":toId,
              "msgtype":"video",
              "video":
              {
                "media_id":mediaId,
                "thumb_media_id":mediaId,
                "title":title,
                "description":desc
              }
            }
    return sendMsg(msgJson)

def sendMusicMsg(toId,url,path,title,desc):
    result = upload(path,'music')
    if 'errcode' in result:
       Logger.e('文件上传失败', result['errmsg'])
       return sendTextMsg(toId,'文件上传失败:'+result['errmsg'])
    mediaId = result['media_id']
    msgJson = {
              "touser":toId,
              "msgtype":"music",
              "music":
              {
                "title":title,
                "description":desc,
                "musicurl":url,
                "hqmusicurl":url,
                "thumb_media_id":mediaId 
              }
            }
    return sendMsg(msgJson)


if __name__ == '__main__':
  #  addServer('qin-1','daniel',123456)
   sendTextMsg('omyqB1uI5qSm5Ypdum43V2zMrTVk','你好')
  #  sendImageMsg('omyqB1uI5qSm5Ypdum43V2zMrTVk','../test.png')
  #  servers = getServersList()
  #  print(servers)