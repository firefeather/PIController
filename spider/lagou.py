# -*- coding: utf-8 -*-
# 爬取拉勾网职位信息

import time,os,random
from openpyxl import Workbook
import pymysql.cursors
from fetch import post

citys = ['武汉','北京', '深圳', '杭州'] 

def _getFilePath():
    if not os.path.exists("./Job/"):
        os.mkdir("./Job/")
    return "./Job/"

def getJson(url, page, lang_name):
    '''返回当前页面的信息列表'''
    headers = {
        'Host': 'www.lagou.com',
        'Connection': 'keep-alive',
        'Content-Length': '23',
        'Origin': 'https://www.lagou.com',
        'X-Anit-Forge-Code': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Anit-Forge-Token': 'None',
        'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }
    data = {'first': 'false', 'pn': page, 'kd': lang_name}
    json = post(url, data, headers=headers)
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = []
        info.append(i.get('companyShortName', '无'))
        info.append(i.get('companyFullName', '无'))
        info.append(i.get('industryField', '无'))
        info.append(i.get('companySize', '无'))
        info.append(i.get('salary', '无'))
        info.append(i.get('city', '无'))
        info.append(i.get('education', '无'))
        info.append(i.get('workYear', '无'))
        info.append(i.get('positionName', '无'))
        info.append(i.get('createTime', '无'))
        info.append(i.get('positionAdvantage', '无'))
        info_list.append(info)
    return info_list


def getJobInfo(jobName):
    wb = Workbook()  # 打开 excel 工作簿
    fileName = _getFilePath()+'{} {}职位信息.xlsx'.format(time.strftime('%Y-%m-%d %H:%M', time.localtime()),jobName)
    for city in citys:
        if city == citys[0]:
           ws = wb.active
        else:
           ws = wb.create_sheet()
        page = 1
        ws.title = city
        ws.sheet_properties.tabColor = "1072BA"
        ws.append(['【公司简称】','【公司全名】','【所属行业】','【公司规模】','【薪资待遇】','【所在城市】','【学历要求】','【工作时间】','【岗位名称】','【发布时间】','【公司优势】'])
        url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(city)
        while page < 4:   # 每个城市3页信息
            info = getJson(url, page, jobName)
            print(city, '获取第', page,'页成功')
            page += 1
            time.sleep(random.randint(10, 20))
            for row in info:
                ws.append(row)
    wb.save(fileName)
    print('获取',jobName,'职位信息完毕')
    return fileName