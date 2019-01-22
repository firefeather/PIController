# -*- coding: utf-8 -*-
# 定时任务
import os, logging, time, datetime
from config import getGeneralConfig
from logger import Logger
from utils.timer import Timer

config = getGeneralConfig()

def _clearLog():
    logPath = config['log_path']
    logSaveDays = config['log_save_days']

    def _removeLog(filename, timedifference):
        date = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        now = datetime.datetime.now()
        if (now - date).seconds > timedifference:
            if os.path.exists(filename):
                os.remove(filename)
                Logger.v('自动删除日志文件:' + filename)

    def removeLogsBefore():
        ITEMS = os.listdir(logPath)
        NEWLIST = []
        for names in ITEMS:
            if names.endswith(".log"):
                NEWLIST.append(logPath + names)
        for names in NEWLIST:
            _removeLog(names, int(logSaveDays) * 24 * 60 * 60)
    
    Timer(removeLogsBefore, 86400).start()


def startTasks():
    _clearLog()