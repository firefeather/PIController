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

def release_weibo(content):
    main_button = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#weibo_top_public > div > div > div.gn_position > div.gn_nav > ul > li:nth-child(1) > a'))
    )
    main_button.click()
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


if __name__=='__main__':
    login()
    time.sleep(6)
    release_weibo('今天天气不错啊')
