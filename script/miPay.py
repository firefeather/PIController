# @Description: 参与小米钱包福利专区的抽奖
import os
import sys
import selenium
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
        Logger.v('小米登录验证码识别结果:'+code)
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
    # try:
    # 	sleep(1)
    # 	# 换成招商银行卡支付
    # 	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)=''])[1]/following::span[4]").click()
    # except:
    # 	driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='一分钱拼好运优惠券'])[1]/following::button[1]").click()
    # 	driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)=''])[1]/following::span[4]").click()
    # 	pass
    # for i in range(3, 5):
    # 	path = "(.//*[normalize-space(text()) and normalize-space(.)=''])[" + str(i) + "]/following::span[2]"
    # 	a = driver.find_element_by_xpath(path)
    # 	# 中信银行信用卡 尾号8311
    # 	if a.text == '招商银行信用卡 尾号2508':
    # 		a.click()
    # 		break
    sleep(1)
    # 输入支付密码
    try:
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)=''])[2]/following::button[1]"
        ).click()
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
        sleep(1)
        driver.find_element_by_link_text("确定").click()
        sleep(1)
        result = True
    except Exception as e:
        Logger.e('小米支付失败',e)
    finally:
        return result


def goodLuck(driver):  #一分钱抽奖
    driver.get('https://s.pay.xiaomi.com')
    paySuccessCount = 0
    while True:
        try:
            button = driver.find_element_by_link_text("立即参与")
        except:
            break
        button.click()
        sleep(2)
        payResult = pay(driver)
        if payResult:
           paySuccessCount += 1
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

    # 结束后发送通知
    noticeTxt='共有' + str(total) + '个活动, 新参加了' +str(paySuccessCount)+ '个活动,共参与了' + str(count) + '个活动.'
    Logger.n('小米抽奖活动',noticeTxt)
    return driver


def getUpEarly(driver):
    driver.get('https://s.pay.xiaomi.com')
    try:
        button = driver.find_element_by_link_text("早起打卡")
        button.click()
        sleep(2)
        driver.find_element_by_class_name("btn-daka").click()
        sleep(3)
        try:
            driver.find_element_by_class_name("btn-daka")#打卡按钮还在  说明没有跳转
            Logger.v('小米早期打卡等待中或打卡成功')
        except:
            payResult = pay(driver)
            if payResult:
               Logger.v('小米早起打卡支付成功')
    except Exception as e:
          Logger.e('小米早起打卡失败',e)


def startMiPay(username,password,onlyDaka=False):
    driver = login(username,password)
    # driver = login('102734075@qq.com', 'ibelieve5')
    try:
        getUpEarly(driver)
        if not onlyDaka:
           goodLuck(driver)
    except Exception as e:
        Logger.e('小米支付任务异常',e)
    finally:
        sleep(10)
        driver.quit()
        Logger.v('小米支付任务执行完毕')

if __name__ == '__main__':
    startMiPay('18671717521', 'qdq19910913qdq')
