#!/usr/bin/env python
# encoding: utf-8

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException
from phone.utils.key_code import *
from phone.utils.adb_utils import AdbUtils
from phone.utils.device_utils import *
from phone.utils.airtest_utils import *
from phone.wechat.Ids import *
import time
from logger import Logger

# -----------------大目标App--------------------------------
package_name = 'com.tencent.mm'
activity = '.ui.LauncherUI'


class Wechat(object):
    def __init__(self):
        try:
            self.poco = AndroidUiautomationPoco(screenshot_each_action=False)
            self.adb = AdbUtils()
            auto_setup(__file__)
            self.connected = True
        except Exception as e:
            Logger.e('连接设备失败', e)
            self.connected = False
        self.prepared = False

    def runFunc(self, funcName, **args):
        if not self.connected:
            Logger.e('连接设备失败', '无法执行相关功能')
            return
        self._pre()
        if not self.prepared:
            return
        func = getattr(self, funcName, None)
        if not func is None:
            func(**args)

    def _exit(self):
        home()
        self.adb.sendKeyEvent(POWER)
        self.poco.stop_running()

    def _pre(self):
        if not self.adb.isInstall(package_name):
            Logger.e('未安装{}'.format(package_name), '无法执行微信相关功能')
            return
        self.prepared = True
        #解锁手机
        self.adb.unlockPhone()
        # # 删除缓存文件
        # remove_dir('./temp/')
        home()
        # stop_app(package_name)
        start_target_app(package_name, activity)

    def _toHomePage(self):
        sleep(1)
        if self.poco(id_wechat_bottom_tabs).exists():
            return
        else:
            self.adb.sendKeyEvent(BACK)
            self._toHomePage()

    def __toUserFromSearch(self, user):
        self.poco(id_wechat_search_btn).click()
        self.poco(id_wechat_search_txt).wait_for_appearance()
        perform_view_input(self.poco, id_wechat_search_txt, user)
        self.poco(id_wechat_search_result_list).wait_for_appearance()
        items = self.poco(id_wechat_search_result_list).children()
        for item in items:
            try:
                item_info_text = item.offspring(
                    id_wechat_search_result_item_txt).get_text().strip()
                if item_info_text == user:
                    item.click()
                    return True
            except Exception as e:
                print(e)
        return False

    def __toUserFromRecent(self, user):
        self.poco(id_wechat_recent_message_list).wait_for_appearance()
        items = self.poco(id_wechat_recent_message_list).children()
        for item in items:
            try:
                item_info_text = item.child().child().offspring(
                    id_wechat_recent_message_item_txt).get_text().strip()
                if item_info_text == user:
                    item.click()
                    return True
            except Exception as e:
                print(e)
        return False

    def _goToUser(self, user):
        self._toHomePage()
        self.poco(id_wechat_tab1_btn).click()
        return self.__toUserFromRecent(user) or self.__toUserFromSearch(user)

    def _sendText(self, to, text):
        if to is None:
            Logger.e('发送微信失败', '未指定对象,无法发送')
            return
        if text is None:
            Logger.e('发送微信失败', '发送内容为空无法发送')
            return
        if not self._goToUser(to):
            Logger.e('发送微信失败', '未找到指定对象')
            return
        self.poco(id_wechat_message_txt).wait_for_appearance()
        perform_view_input(self.poco, id_wechat_message_txt, text)
        self.poco(id_wechat_message_send_btn).click()
        Logger.v('发送微信消息:{},给{}成功'.format(text, to))

    def _makeVideoCall(self, to):
        if to is None:
            Logger.e('拨打微信电话失败', '未指定对象')
            return
        if not self._goToUser(to):
            Logger.e('拨打微信电话失败', '未找到指定对象')
            return
        self.poco(id_wechat_message_txt).wait_for_appearance()
        self.poco(id_wechat_message_more_entrance_btn).click()
        self.poco(id_wechat_message_more_func_list).wait_for_appearance()
        items = self.poco(id_wechat_message_more_func_list).children()
        for item in items:
            try:
                item_info_text = item.child().child().offspring(
                    id_wechat_message_more_func_item_txt).get_text().strip()
                if item_info_text == '视频通话':
                    item.click()
                    sleep(1)
                    if self.poco(id_wechat_calls_select_list).exists():
                        self.poco(id_wechat_calls_item_video).click()
                    Logger.v('拨打微信电话成功')
                    break
            except Exception as e:
                print(e)


def sendText(text, to='老板'):
    wechat = Wechat()
    wechat.runFunc('_sendText', to=to, text=text)


def makeVideoCall(to='老板'):
    wechat = Wechat()
    wechat.runFunc('_makeVideoCall', to=to)


if __name__ == '__main__':
    sendText('hello')
