# -*- coding: utf-8 -*-
# 获取服务器设备信息

import os, platform, time


def getCPUtemp():
    temp = os.popen('vcgencmd measure_temp').readline()
    tempfloat = float(temp.replace('temp=', '').replace('\'C\n', '')) 
    return tempfloat


def getCPUusage():
    #calculate CPU with two short time, time2 - time1
    time1 = os.popen('cat /proc/stat').readline().split()[1:5]
    time.sleep(0.2)
    time2 = os.popen('cat /proc/stat').readline().split()[1:5]
    deltaUsed = int(time2[0]) - int(time1[0]) + int(time2[2]) - int(time1[2])
    deltaTotal = deltaUsed + int(time2[3]) - int(time1[3])
    cpuUsage = float(deltaUsed) / float(deltaTotal) * 100
    return cpuUsage


def getRAM():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:4])


def getDisk():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return (line.split()[1:5])


def getSystemInfo():
    result = ''
    if platform.system() == 'Linux':
        cpuTemp = getCPUtemp()
        cpuUsage = getCPUusage()
        RAM_stats = getRAM()
        DISK_stats = getDisk()
        result = '当前设备信息:\n\n' + ('CPU温度: %.1f ℃,\n' % cpuTemp) + (
            'CPU使用率: %.1f' % cpuUsage + ' %,\n') + (
                '总内存: %.1f MB,已使用: %.1f MB,剩余: %.1f MB,\n' %
                (round(int(RAM_stats[0]) / 1024, 1),
                 round(int(RAM_stats[1]) / 1024, 1),
                 round(int(RAM_stats[2]) / 1024, 1))) + (
                     '总硬盘: %s B,已使用: %s B,剩余: %s B,\n' %
                     (DISK_stats[0], DISK_stats[1], DISK_stats[2]))
    else:
        result = '暂不支持获取此设备信息'
    return result
