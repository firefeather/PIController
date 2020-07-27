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
from script.baiduDog import autoCollect
from script.toutiaoLottery import autoLottery
from script.toutiaoLottery2 import autoJoinLottery
from phone.target.target import autoFollow

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

def _startBaiduCollet(fromUser=False):  #百度莱茨狗自动收元气
    Logger.v('开始执行百度自动收元气')
    autoCollect()
    if not fromUser:
        scheduler.remove_job(job_ids['_startBaiduCollet'])
        _addBaiduJob()

def _startToutiaoLottery(fromUser=False):  #头条全民抽奖
    Logger.v('开始执行头条全民抽奖')
    autoLottery()
    if not fromUser:
        scheduler.remove_job(job_ids['_startToutiaoLottery'])
        _addTouTiaoJob()

def _startToutiaoLottery2(fromUser=False):  #头条人人抽奖
    Logger.v('开始执行头条人人抽奖')
    autoJoinLottery()
    if not fromUser:
        scheduler.remove_job(job_ids['_startToutiaoLottery2'])
        _addTouTiaoJob2()

def _startMiZhongchou(fromUser=False):  #发送小米众筹产品信息
    Logger.v('开始获取小米众筹产品信息并发送')
    info = getGoodList()
    sendTextMsg(MANAGER.Id, info)

def _startSmallTarget(fromUser=False):  #达目标自动围观
    Logger.v('开始执行达目标自动围观')
    result = autoFollow()
    if result.new_money>0:
        Logger.v('达目标围观新分得了{}元钱'.format(result.new_money))
        sendTextMsg(MANAGER.Id, '达目标围观新分得了{}元钱'.format(result.new_money))



def _addWangyiJob():
    job_ids['_startWangyiCollet'] = scheduler.add_job(
        func=_startWangyiCollet,
        trigger='cron',
        day_of_week='0-6',
        hour=random.randint(8, 22),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)  #每天8-22点随机时刻收取网易星球黑钻
    ).id

def _addBaiduJob():
    job_ids['_startBaiduCollet'] = scheduler.add_job(
        func=_startBaiduCollet,
        trigger='cron',
        day_of_week='0-6',
        hour=random.randint(8, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)  #每天8-23点随机时刻收取百度元气
    ).id

def _addTouTiaoJob():
    job_ids['_startToutiaoLottery'] = scheduler.add_job(
        func=_startToutiaoLottery,
        trigger='cron',
        day_of_week='0-6',
        hour=random.randint(10, 22),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)  #每天8-23点随机时刻参与头条抽奖
    ).id

def _addTouTiaoJob2():
    job_ids['_startToutiaoLottery2'] = scheduler.add_job(
        func=_startToutiaoLottery2,
        trigger='cron',
        day_of_week='0-6',
        hour=random.randint(8, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)  #每天8-23点随机时刻参与头条抽奖
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

def _addSmallTargetJob():
    job_ids['_startSmallTarget'] = scheduler.add_job(
        func=_startSmallTarget,
        trigger='cron',
        day_of_week='0-6',
        hour=22,
        minute=random.randint(0, 30),
        second=random.randint(0, 59)  #每天晚上10点执行达目标
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
    # _addMiDakaJob()
    # _addMiTaskJob()
    _addWangyiJob()
    # _addMiZhongchouJob()
    _addBaiduJob()
    _addTouTiaoJob()
    _addTouTiaoJob2()
    # _addSmallTargetJob()

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