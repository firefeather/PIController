# @Description: 参与小米钱包福利专区的抽奖
import os
import sys
import selenium
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep, strftime
# 验证码识别模块
from PIL import Image
from utils.chaojiying import imageToCode
from logger import Logger
import platform


#该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
def isElementExist(driver, id):
    flag = True
    try:
        driver.find_element_by_id(id)
    except:
        flag = False
    finally:
        return flag


# 验证码
def check(driver):
    if isElementExist(driver, 'captcha-img'):
        Logger.v('小米登录需要验证码,正在尝试自动识别验证码')
        #获取截图
        driver.get_screenshot_as_file('screenshot.png')

        #获取指定元素位置
        element = driver.find_element_by_id('captcha-img')
        left = int(element.location['x']) + 250
        top = int(element.location['y']) + 340
        right = int(element.location['x'] + element.size['width']) + 375
        bottom = int(element.location['y'] + element.size['height']) + 390

        # 通过Image处理图像
        im = Image.open('screenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save('code.png')
        code = imageToCode('code.png')
        Logger.v('小米登录验证码识别结果:' + code)
        driver.find_element_by_id("captcha-code").send_keys(code)
        driver.find_element_by_id("login-button").click()
    else:
        Logger.v('小米登录无需验证码,已登录成功')


def login(username, password):
    options = webdriver.ChromeOptions()
    if platform.system() == 'Linux':
        # 以 headless 方案运行
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(5)  # 隐性等待，最长等5秒
    driver.set_window_size(400, 1170)
    driver.get('https://s.pay.xiaomi.com')

    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("pwd").send_keys(password)
    driver.find_element_by_id("login-button").click()
    check(driver)
    return driver


def pay(driver):
    result = False
    sleep(1)
    # 输入支付密码
    try:
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)=''])[2]/following::button[1]"
        ).click()
        sleep(2)
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)=''])[1]/following::li[5]"
        ).click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)=''])[1]/following::li[8]"
        ).click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)=''])[1]/following::li[4]"
        ).click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)=''])[1]/following::li[5]"
        ).click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)=''])[1]/following::li[2]"
        ).click()
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)=''])[1]/following::li[1]"
        ).click()
        sleep(2)
        driver.find_element_by_class_name("ui-form-confirm-button").click()
        sleep(1)
        result = True
    except Exception as e:
        Logger.e('小米支付失败', e)
    finally:
        return result

def pay2(driver):
    result = False
    sleep(1)
    # 输入支付密码
    try:
        driver.find_element_by_xpath('/html[1]/body[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/input[1]').send_keys(584521)
        sleep(2)
        driver.find_element_by_link_text("确定").click()
        sleep(1)
        result = True
    except Exception as e:
        Logger.e('小米支付失败', e)
    finally:
        return result


def goodLuck(driver):  #一分钱抽奖
    driver.get('https://s.pay.xiaomi.com')
    paySuccessCount = 0
    while True:
        free = False
        try:
            button = driver.find_element_by_link_text("立即参与")
            button.click()
            if '暂无' not in driver.find_elements_by_class_name('coupon-num')[0].text:
                sleep(2)
                freeRadio = driver.find_elements_by_class_name('coupons')
                if len(freeRadio) > 0:
                    freeRadio[0].click()
                    sleep(1)
                    juans = driver.find_elements_by_class_name('coupon')
                    juans[0].click()
                    free = True
        except Exception as e:
            break
        sleep(2)
        driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[1]/div[1]/div[7]/div[1]/div[2]/div[5]/button[1]').click()
        sleep(2)
        if not free:
            payResult = pay(driver)
            if payResult:
                paySuccessCount += 1
        else:
            paySuccessCount += 1
        sleep(1)
        driver.find_element_by_link_text("继续参与").click()
        driver.get(driver.current_url)
        sleep(2)
        driver.refresh()
    sleep(2)

    total = len(driver.find_elements_by_class_name("activity-wrap"))
    count = len(driver.find_elements_by_link_text("已参与"))

    driver.find_element_by_xpath(
        u"(.//*[normalize-space(text()) and normalize-space(.)='拼好运'])[1]/preceding::img[3]"
    ).click()

    if count > 0:
        # 结束后发送通知
        noticeTxt = '共有' + str(total) + '个活动, 新参加了' + str(
            paySuccessCount) + '个活动,共参与了' + str(count) + '个活动.'
        Logger.v('小米抽奖活动'+ noticeTxt)
    return driver

def goodLuckAll(driver):  #一次性参与所有的一分钱抽奖
    driver.get('https://s.pay.xiaomi.com')
    all = driver.find_elements_by_class_name("alert-info")
    if len(all) > 0:
        btn = all[0]
        count = btn.text.strip().split('，')[0][3:-6]
        btn.click()
        sleep(1)
        driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[1]/div[1]/div[7]/div[1]/div[2]/div[4]/button[1]').click()
        sleep(2)
        payResult = pay(driver)
        if payResult:
            # 结束后发送通知
            noticeTxt = '统一参与了' + str(count) + '个活动.'
            Logger.v('小米抽奖活动'+ noticeTxt)
        sleep(1)
        driver.find_element_by_link_text("继续参与").click()

def getUpEarly(driver, onlyDaka=False):
    driver.get('https://s.pay.xiaomi.com')
    try:
        button = driver.find_element_by_link_text("早起打卡")
        button.click()
        sleep(2)
        driver.find_element_by_class_name("btn-daka").click()
        sleep(3)
        if not onlyDaka:  #不只是打卡 则尝试支付明天的
            try:
                driver.find_element_by_class_name("btn-daka")  #打卡按钮还在  说明没有跳转
                Logger.v('小米早期打卡等待中或打卡成功')
            except:
                payResult = pay(driver)
                if payResult:
                    Logger.v('小米早起打卡支付成功')
    except Exception as e:
        Logger.e('小米早起打卡失败', e)


def startMiPay(username, password, onlyDaka=False):
    driver = login(username, password)
    # driver = login('102734075@qq.com', 'ibelieve5')
    try:
        getUpEarly(driver, onlyDaka)
        if not onlyDaka:
            today = datetime.date.today()
            if today.day != 5 and today.day != 20:
               goodLuckAll(driver)
            else:
               goodLuck(driver)
    except Exception as e:
        Logger.e('小米支付任务异常', e)
    finally:
        sleep(5)
        # driver.quit()
        Logger.v('小米支付任务执行完毕')


if __name__ == '__main__':
    startMiPay('18671717521', 'qdq19910913qdq')
