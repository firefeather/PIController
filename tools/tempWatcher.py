# -*- coding: utf-8 -*-
#自动风扇控制程序，使用wiringPi的gpio命令来操作GPIO
from tools.systemInfo import getCPUtemp
from logger import Logger
import time, subprocess

TEMP_POWER_OFF = 80  #关闭计算机的温度
TEMP_POWER_WARN = 70  #报警温度


def watchTemp():
    cupTemp = getCPUtemp()
    if cupTemp >= TEMP_POWER_OFF:
        Logger.n('温度过高', '即将关机,当前CPU温度: %.1f ℃' % cupTemp)
        time.sleep(2)
        status, output = subprocess.getstatusoutput('poweroff')
        result = ('关机成功:' if status == 0 else '关机失败:') + output
        Logger.v(result)
    elif cupTemp >= TEMP_POWER_WARN:
        Logger.n('温度超高预警', '温度过高,当前CPU温度: %.1f ℃' % cupTemp)
