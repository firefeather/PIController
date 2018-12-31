# -*- coding:utf-8 -*-
#百度语音合成

from aip import AipSpeech
from config import getVoiceConfig
from fetch import get,download
import platform

voiceFile = 'auido.mp3'

voiceConfig = getVoiceConfig()
appId = voiceConfig['appid']
apiKey = voiceConfig['apikey']
secretKey = voiceConfig['secret_key']

client = AipSpeech(appId, apiKey, secretKey)

def voice(text):
    result  = client.synthesis(text, 'zh', 1, {
    'vol': 10,#String	音量，取值0-15，默认为5中音量
    'per':4,#	String	发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
    # 'pit':6,#String	音调，取值0-9，默认为5中语调
    # 'spd':6	#String	语速，取值0-9，默认为5中语速
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
      with open(voiceFile, 'wb') as f:
        f.write(result)
    else:
      print(text,'合成失败',result['error_msg'])
    playSound()
    
def say(text):
    url = 'http://tts.baidu.com/text2audio?idx=1&tex={}&cuid=baidu_speech_demo&cod=2&lan=zh&ctp=1&pdt=1&spd=5&per=4&vol=5&pit=5'.format(text)
    result = download(url)
    # print('1111',result)
    with open(voiceFile, 'wb') as f:
        for chunk in result.iter_content(chunk_size=1024):
          if chunk:
            f.write(chunk)
    playSound()

def playSound():
    if platform.system() == 'Linux':
       import subprocess
       subprocess.Popen(['mplayer',voiceFile])
    else:
       import pygame,time
       pygame.mixer.init()
       track = pygame.mixer.music.load(voiceFile)
       #播放音乐10秒后停止
       pygame.mixer.music.play()
       time.sleep(10)
       pygame.mixer.music.stop()

if __name__ == '__main__':
    print(say('你好'))