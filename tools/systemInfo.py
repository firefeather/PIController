# -*- coding: utf-8 -*-
# 获取服务器设备信息

import os, platform, time


def getCPUtemp():
    temp = os.popen('vcgencmd measure_temp').readline()
    tempfloat = temp.replace('temp=', '').replace('\'C\n', '')
    return tempfloat


def getCPUusage():
    return str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())


def getRAM():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

def getDisk():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])



def getSystemInfo():
    result = ''
    if platform.system() == 'Linux':
        cpuTemp = getCPUtemp()
        cpuUsage = getCPUusage()
        RAM_stats = getRAM()
        DISK_stats = getDisk()
        result = '当前设备信息:\n\n' + ('CPU温度:%.1s ℃,\n' % cpuTemp) + (
            'CPU使用率:%.1s' % cpuUsage + ' %,\n') + (
                '总内存:%.1f MB,已使用:%.1f MB,剩余:%.1f MB,\n' %
                (round(int(RAM_stats[0]) / 1000,1), round(int(RAM_stats[1]) / 1000,1), round(int(RAM_stats[2]) / 1000,1))) + (
                    '总硬盘:%s GB,已使用:%s GB,剩余:%s GB,\n' %
                    (DISK_stats[0], DISK_stats[1], DISK_stats[2]))
    else:
        result = '暂不支持获取此设备信息'
    return result
