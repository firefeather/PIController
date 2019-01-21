#coding=utf-8

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)

def login():
    browser.get('https://weibo.com/')
    time.sleep(2)
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#loginname'))
    )
    # username为用户名
    input.send_keys('18671717521')
    input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#pl_login_form > div > div:nth-child(3) > div.info_list.password > div > input'))
    )
    time.sleep(1)
    # password为密码
    input.send_keys('qdq19910913qdq')
    button = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#pl_login_form > div > div:nth-child(3) > div.info_list.login_btn > a'))
    )
    time.sleep(2)
    button.click()

def sendWeibo(content):
    result=''
    try:
        login()
        time.sleep(6)
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#v6_pl_content_publishertop > div > div.input > textarea'))
        )
        input.clear()
        now = time.strftime('%Y-%m-%d')
        weibo_content=content+'\n---------本微博由树莓派发送<'+now+'>'
        input.send_keys(weibo_content)
        release_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#v6_pl_content_publishertop > div > div.func_area.clearfix > div.func > a'))
        )
        time.sleep(3)
        release_button.click()
        time.sleep(3)
        browser.quit()
        result='发送成功'
    except Exception as e:
        print('发送微博失败:',e)
        result='发送失败'
    return result


if __name__=='__main__':
    login()
    time.sleep(6)
    sendWeibo('今天天气不错啊')
