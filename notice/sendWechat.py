# coding:utf-8
#通过微信公众号发送微信消息
from wechat.tocken import Tocken
from fetch import get,postJson
from wechat.media import uplaod

def sendMsg(msgJson):
    accessToken = Tocken().get_access_token()
    postUrl = ("https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % accessToken )
    result = postJson(postUrl,msgJson)
    return result

def sendTextMsg(content,toId):
    msgJson = {
              "touser":toId,
              "msgtype":"text",
              "text":
                  {
                  "content":content
                  }   
            }
    return sendMsg(msgJson)

def sendImageMsg(toId,path):
    result = uplaod(path,'image')
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
    result = uplaod(path,'voice')
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
    result = uplaod(path,'video')
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
    result = uplaod(path,'music')
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
  #  sendTextMsg('omyqB1uI5qSm5Ypdum43V2zMrTVk','你好')
   sendImageMsg('omyqB1uI5qSm5Ypdum43V2zMrTVk','../test.png')
  #  servers = getServersList()
  #  print(servers)