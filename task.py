# -*- coding: utf-8 -*-
# 定时任务
import os, logging, time, datetime,random
from config import getGeneralConfig
from logger import Logger
from script.miPay import startMiPay
from apscheduler.schedulers.blocking import BlockingScheduler

config = getGeneralConfig()

def _clearLog():
    Logger.v('开始执行日志清理')
    logPath = config['log_path']
    logSaveDays = config['log_save_days']

    def _removeLog(filename, timedifference):
        date = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        now = datetime.datetime.now()
        if (now - date).seconds > timedifference:
            if os.path.exists(filename):
                os.remove(filename)
                Logger.v('自动删除日志文件:' + filename)

    ITEMS = os.listdir(logPath)
    NEWLIST = []
    for names in ITEMS:
        if names.endswith(".log"):
                NEWLIST.append(logPath + names)
        for names in NEWLIST:
            _removeLog(names, int(logSaveDays) * 24 * 60 * 60)
    
def _startMiDaka():#只执行打卡
    Logger.v('开始执行小米早起打卡')
    username = config['mi_user_name']
    password = config['mi_pass_word']
    startMiPay(username,password,True)

def _startMiTask():#执行打卡和一分钱抽奖
    Logger.v('开始执行小米抽奖和明日打卡')
    username = config['mi_user_name']
    password = config['mi_pass_word']
    startMiPay(username,password,False)

def startTasks():
    scheduler = BlockingScheduler()
    scheduler.add_job(func=_clearLog, trigger='interval', days=1)#每天执行一次清理日志任务
    scheduler.add_job(func=_startMiDaka,trigger='cron',day_of_week ='0-6',hour = 6,minute = 0,second = 0)#每天早上6点执行小米早起打卡
    scheduler.add_job(func=_startMiTask,trigger='cron',day_of_week ='0-6',hour = random.randint(11,20),minute = random.randint(1,59),second = random.randint(1,59))#每天随机时间点执行小米抽奖
    
    scheduler.start()

if __name__ == '__main__':
    _startMiTask()