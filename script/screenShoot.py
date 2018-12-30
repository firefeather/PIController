# -*- coding: utf-8 -*-
# 截屏

import os
import platform
from time import time

def _GetImagePath():
    if not os.path.exists("./ScreenShoot/"):
        os.mkdir("./ScreenShoot/")
    return "./ScreenShoot/"


def getScreenImg():
    imPath = _GetImagePath()
    imName = "{}{}.{}".format(imPath, int(time()), "png")
    im = None
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        try:
            from PIL import ImageGrab
            im = ImageGrab.grab()
        except OSError as e:
            return "截图失败，请重试。"

    elif platform.system() == 'Linux':
        try:
            import pyscreenshot as ImageGrab
            im = ImageGrab.grab()
        except Exception as e:
            return "截图失败，请重试。"
    im.save(imName)
    if os.path.exists(imName):
        return imName
    else:
        return "截图失败，请重试。"
