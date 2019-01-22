# -*- coding:utf-8 -*-
#定时器
import datetime, signal, threading, sys, time
from logger import Logger

class Timer:
    def __init__(self, func, space):
        self.func = func
        self.space = space

    def start(self):
        def quit(signum, frame):
            sys.exit()

        def process_fun():
            while True:
                self.func()
                time.sleep(self.space)

        try:
            signal.signal(signal.SIGINT, quit)
            signal.signal(signal.SIGTERM, quit)
            p = threading.Thread(target=process_fun)
            #注册成为主进程
            p.setDaemon(True)
            p.start()
        except Exception as e:
            Logger.e('启动定时器失败',e)
