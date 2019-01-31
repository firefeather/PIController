# -*- coding:utf-8 -*-
#文字转语音(离线)

import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'zh')
    # voices = engine.getProperty('voices')
    # for voice in voices:
    #   print('voice',voice.id)
    #   engine.setProperty('voice', voice.id)
    #   engine.say('你好,我爱你')
    # engine.setProperty('rate', 200)
    # volume = engine.getProperty('volume')
    # print('volume',volume)
    # engine.setProperty('volume', 2)
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
   speak('你好吗')
   speak('hello world')
