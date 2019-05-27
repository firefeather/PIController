# -*- coding: utf-8 -*-
import socket,datetime
from utils.speaker import speak

def isNetOK(testserver=('www.qq.com',443)):
    s=socket.socket()
    s.settimeout(3)
    try:
        status = s.connect_ex(testserver)
        if status == 0:
            s.close()
            return True
        else:
            if(isDayTime()):
                speak('连接到测试服务器失败')
            return False
    except Exception as e:
        if(isDayTime()):
            speak('网络连接失败')
        return False

def isDayTime():
    now = datetime.datetime.now()
    hour = now.hour
    if hour>8 and hour <23:
       return True
    else:
       return False

if __name__ == '__main__':
    print(isDayTime())