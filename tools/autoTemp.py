# -*- coding: utf-8 -*-
#自动风扇控制程序，使用wiringPi的gpio命令来操作GPIO
from tools.systemInfo import getCPUtemp
from logger import Logger
from RPi import GPIO as gpio  #注意RPi中的i是小写的

FAN_GPIO = 15  #控制风扇的GPIO
TEMP_ON = 60  #开启风扇的温度
TEMP_OFF = 45  #关闭风扇的温度

global IS_ON  #风扇是否开启
IS_ON = False

#BOARD编号方式，基于插座引脚编号
gpio.setmode(gpio.BOARD)

#设置哪个引脚为输出模式
gpio.setup(FAN_GPIO, gpio.OUT)


def autoControlTemp():
    try:
        cupTemp = getCPUtemp()
        global IS_ON
        if (not IS_ON) and (cupTemp >= TEMP_ON):  #如果之前关闭并且温度高了，就启动风扇
            gpio.output(FAN_GPIO, 1)
            IS_ON = True
            Logger.v('开启风扇,当前CPU温度: %.1f ℃' % cupTemp)
        elif IS_ON and (cupTemp <= TEMP_OFF):  #如果之前开启并且温度降下来了，就关闭风扇
            gpio.output(FAN_GPIO, 0)
            IS_ON = False
            Logger.v('关闭风扇,当前CPU温度: %.1f ℃' % cupTemp)
        else:
            Logger.v('风扇状态:'+str(IS_ON)+('当前CPU温度: %.1f ℃' % cupTemp))
    except Exception as e:
        gpio.cleanup()
        Logger.e('开关风扇失败', e)
