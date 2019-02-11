# -*- coding: utf-8 -*-
# 定时任务
import os, logging, time, datetime, random
from config import getGeneralConfig
from logger import Logger
from script.miPay import startMiPay
from apscheduler.schedulers.background import BackgroundScheduler
from script.wangyiPlanet import autoCollectCoins

config = getGeneralConfig()

scheduler = BackgroundScheduler()

job_ids = {}


def _clearLog():
    Logger.v('开始执行日志清理')
    logPath = config['log_path']
    logSaveDays = config['log_save_days']

    def _removeLog(filename, daysDiff):
        if os.path.exists(filename):
            date = datetime.datetime.fromtimestamp(os.path.getctime(filename))
            now = datetime.datetime.now()
            if (now - date).days > daysDiff:
                os.remove(filename)
                Logger.v('自动删除日志文件:' + filename)

    files = os.listdir(logPath)
    logs = []
    for file in files:
        if file.endswith(".log"):
            logs.append(logPath + file)
        for log in logs:
            _removeLog(log, int(logSaveDays))


def _startMiDaka():  #只执行打卡
    Logger.v('开始执行小米早起打卡')
    username = config['mi_user_name']
    password = config['mi_pass_word']
    startMiPay(username, password, True)
    scheduler.remove_job(job_ids['_startMiDaka'])
    _addMiDakaJob()


def _startMiTask():  #执行打卡和一分钱抽奖
    Logger.v('开始执行小米抽奖和明日打卡')
    username = config['mi_user_name']
    password = config['mi_pass_word']
    startMiPay(username, password, False)
    scheduler.remove_job(job_ids['_startMiTask'])
    _addMiTaskJob()


def _startWangyiCollet():  #网易星球自动收钻
    Logger.v('开始执行网易星球自动收取钻石')
    autoCollectCoins()
    scheduler.remove_job(job_ids['_startWangyiCollet'])
    _addWangyiJob()


def _addWangyiJob():
    job_ids['_startWangyiCollet'] = scheduler.add_job(
        func=_startWangyiCollet,
        trigger='cron',
        day_of_week='0-6',
        hour=random.randint(8, 22),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)  #每天8-22点随机时刻收取网易星球黑钻
    ).id


def _addMiDakaJob():
    job_ids['_startMiDaka'] = scheduler.add_job(
        func=_startMiDaka,
        trigger='cron',
        day_of_week='0-6',
        hour=6,
        minute=random.randint(0, 30),
        second=random.randint(0, 59)  #每天早上6点-6点半执行小米早起打卡
    ).id


def _addClearLogJob():
    job_ids['_clearLog'] = scheduler.add_job(
        func=_clearLog,
        trigger='cron',
        day_of_week=random.randint(0, 6),
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)  #每周随机时间清理一次日志
    ).id


def _addMiTaskJob():
    job_ids['_startMiTask'] = scheduler.add_job(
        func=_startMiTask,
        trigger='cron',
        day_of_week='0-6',
        hour=random.randint(10, 18),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)  #每天随机时间点执行小米抽奖
    ).id


def startTasks():
    _addClearLogJob()
    _addMiDakaJob()
    _addMiTaskJob()
    _addWangyiJob()

    scheduler.start()


def getJobs():
    # scheduler.print_jobs()
    jobs = scheduler.get_jobs()
    text = ''
    if len(jobs):
        text = '共{}个任务:\n'.format(len(jobs))
        for job in jobs:
            text += str(job) + '\n\n'
    else:
        text = '暂无任务'

    return text


if __name__ == '__main__':
    _startMiTask()