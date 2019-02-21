# -*- coding: utf-8 -*-
#自动风扇控制程序，使用wiringPi的gpio命令来操作GPIO
from tools.systemInfo import getCPUtemp
import subprocess, platform
from logger import Logger

FAN_GPIO = 15  #控制风扇的GPIO
TEMP_ON = 60  #开启风扇的温度
TEMP_OFF = 45  #关闭风扇的温度


def autoControlTemp():
    if platform.system() == 'Linux':
        cupTemp = getCPUtemp()
        code = None
        #如果温度大于50`C，就启动风扇
        if cupTemp >= TEMP_ON:
            code = 0
        #如果温度小于45`C，就关闭风扇
        elif cupTemp <= TEMP_OFF:
            code = 1
        if not code is None:
            status, output = subprocess.getstatusoutput(
                'sudo gpio write {} {}'.format(FAN_GPIO, code))
            result = ('开启风扇' if code == 0 else '关闭风扇') + ('成功:' if status == 0
                                                          else '失败:') + output
            Logger.v(result)
