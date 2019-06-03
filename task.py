# -*- coding: utf-8 -*-
# 定时任务
import os, logging, time, datetime, random, platform
from config import getGeneralConfig
from logger import Logger
from script.miPay import startMiPay
from apscheduler.schedulers.background import BackgroundScheduler
from script.wangyiPlanet import autoCollectCoins
from spider.miCrowdfunding import getGoodList
from notice.sendWechat import sendTextMsg
from users import MANAGER
from tools.weatherWatcher import watchWeather
from tools.netCheck import isNetOK
from tools.tempWatcher import watchTemp

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


def _startMiDaka(fromUser=False):  #只执行打卡
    Logger.v('开始执行小米早起打卡')
    username = config['mi_user_name']
    password = config['mi_pass_word']
    startMiPay(username, password, True)
    if not fromUser:
        scheduler.remove_job(job_ids['_startMiDaka'])
        _addMiDakaJob()


def _startMiTask(fromUser=False):  #执行打卡和一分钱抽奖
    Logger.v('开始执行小米抽奖和明日打卡')
    username = config['mi_user_name']
    password = config['mi_pass_word']
    startMiPay(username, password, False)
    if not fromUser:
        scheduler.remove_job(job_ids['_startMiTask'])
        _addMiTaskJob()


def _startWangyiCollet(fromUser=False):  #网易星球自动收钻
    Logger.v('开始执行网易星球自动收取钻石')
    autoCollectCoins()
    if not fromUser:
        scheduler.remove_job(job_ids['_startWangyiCollet'])
        _addWangyiJob()


def _startMiZhongchou(fromUser=False):  #发送小米众筹产品信息
    Logger.v('开始获取小米众筹产品信息并发送')
    info = getGoodList()
    sendTextMsg(MANAGER.Id, info)


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


def _addMiZhongchouJob():
    job_ids['_addMiZhongchouJob'] = scheduler.add_job(
        func=_startMiZhongchou,
        trigger='cron',
        day_of_week='0-6',
        hour=10,
        minute=30,
        second=0  #每天早上10点发送小米众筹产品信息
    ).id


def _addAutoTempControlJob():  #开启自动温控系统
    from tools.autoTemp import autoControlTemp
    job_ids['_addAutoTempControl'] = scheduler.add_job(
        func=autoControlTemp,
        trigger='interval',
        minutes=1  #每1分钟执行一次
    ).id

def _addTempWatcherJob():  #开启温度监测
    job_ids['_addTempWatcher'] = scheduler.add_job(
        func=watchTemp,
        trigger='interval',
        minutes=5  #每5分钟执行一次
    ).id

def _addNetListenerJob():  #监听网络连接情况
    isNetOK()
    job_ids['_addNetListener'] = scheduler.add_job(
        func=isNetOK,
        trigger='interval',
        minutes=10  #每10分钟执行一次
    ).id

def _addWeatherWatcherJob():  #监听天气情况
    job_ids['_addWeatherWatcherJob'] = scheduler.add_job(
        func=watchWeather,
        trigger='cron',
        day_of_week='0-6',
        hour=22,
        minute=0,
        second=0  #每晚22点查询天气情况
    ).id

def startTasks():
    # if platform.system() == 'Linux':
    #     _addAutoTempControlJob()
    _addTempWatcherJob()
    _addNetListenerJob()
    _addWeatherWatcherJob()

    _addClearLogJob()
    _addMiDakaJob()
    _addMiTaskJob()
    _addWangyiJob()
    _addMiZhongchouJob()

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