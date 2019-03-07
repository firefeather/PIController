# -*- coding: utf-8 -*-
#查询双色球开奖结果

import json,random
from fetch import get

HOST = 'http://www.mxnzp.com/api'

def getSSQResult(number=None):
    API = HOST+('/lottery/ssq/aim_lottery?expect={}'.format(number) if not number is None else '/lottery/ssq/latest')
    result = get(API)
    return result['data']['openCode']