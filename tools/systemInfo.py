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
    #get RAM as list,list[7],[8],[9]:total,used,free
    RAM = os.popen('free').read().split()[7:10]
    #convert kb in Mb for readablility
    total = float(RAM[0]) / 1024
    used = float(RAM[1]) / 1024
    free = float(RAM[2]) / 1024
    return total, used, free


def getDisk():
    #get Disk information,DISK[8],[9],[10],[11]:Size, Used. free, Used %
    DISK = os.popen('df -h /').read().split()[8:12]
    return DISK[0], DISK[1], DISK[2]


def getSystemInfo():
    result = ''
    if platform.system() == 'Linux':
        cpuTemp = getCPUtemp()
        cpuUsage = getCPUusage()
        ramTotal, ramUsed, ramFree = getRAM()
        diskTotal, diskUsed, diskFree = getDisk()
        result = '当前设备信息:\n\n' + ('CPU温度:%.1f ℃,\n' % cpuTemp) + (
            'CPU使用率:%.1f' % cpuUsage + ' %,\n') + (
                '总内存:%.1f MB,已使用:%.1f MB,剩余:%.1f MB,\n' %
                (ramTotal, ramUsed, ramFree)) + (
                    '总硬盘:%.1f MB,已使用:%.1f MB,剩余:%.1f MB,\n' %
                    (diskTotal, diskUsed, diskFree))
    else:
        result = '暂不支持获取此设备信息'
    return result
