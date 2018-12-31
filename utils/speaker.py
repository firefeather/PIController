# -*- coding:utf-8 -*-
#文字转语音(离线)

import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'zh')
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
   speak('你好吗')
   speak('hello world')
