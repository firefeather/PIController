from fetch import get
from utils.baiduVoice import voice
from logger import Logger

HOST = 'https://www.mxnzp.com/api'
IP_TO_ADRESS_API = HOST+'/ip/self'
WEATHER_API = HOST+'/weather/forecast/'

global adress
adress = None

def getAdress():
    global adress
    if adress is None:
       res = get(IP_TO_ADRESS_API)
       adress = res['data']
    return adress

def watchWeather():
    Logger.v('开始查询最近天气')
    adr = getAdress()
    if adress is None:
       Logger.e('获取本机地址信息失败','可能是网络问题或接口不可用')
    city = adr['city'] or '洪山'
    if not city is None:
       res = get(WEATHER_API+city)
       forecasts = res['data']['forecasts']
       result = city + '有异常天气预警:\n'
       for index in range(0, len(forecasts)):
           if index == 0 or index > 2:
              continue
           forecast = forecasts[index]
           date = forecast['date']
           dayWeather = forecast['dayWeather']
           nightWeather = forecast['nightWeather']
           dayTemp = forecast['dayTemp']
           nightTemp = forecast['nightTemp']
           dayWindDirection = forecast['dayWindDirection']
           dayWindPower = forecast['dayWindPower']
           def formatWeather():
              return '白天:'+dayWeather+\
                          ',温度:'+dayTemp+\
                        ',夜间:'+nightWeather+\
                          ',温度:'+nightTemp+\
                          ','+dayWindDirection+\
                          '风:'+dayWindPower+\
                            '.\n'
           if index == 1:
              date = '明天'
           elif index == 2:
              date = '后天'
           weather = ''
           if '雨' in dayWeather or '雪' in dayWeather or '雹' in dayWeather:
              weather += date+'白天天气异常:'+dayWeather+'.'
           if '雨' in nightWeather or '雪' in nightWeather or '雹' in nightWeather:
              weather += date+'夜间天气异常:'+nightWeather+'.'
           try:
              if int(dayTemp.split('℃')[0]) < 0 or int(dayTemp.split('℃')[0]) > 35:
                  weather += date+'白天有高温:'+dayTemp+'.'
              if int(dayWindPower.split('级')[0]) > 5:
                  weather += date+'白天有大风:'+dayWindPower+'.'
           except Exception as e:
              Logger.e('天气数据解析错误',e)
           if len(weather) > 0:
              result += weather+date +'详细天气:'+formatWeather()
       if len(result) > 15:
           result += '请注意防范!\n'
           Logger.v('有异常天气!'+result)
           voice(result)
       else:
           Logger.v('未发现异常天气')






