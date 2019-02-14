# -*- coding: utf-8 -*-
# 获取当日小米优品众筹产品

from fetch import get
from datetime import datetime

url = 'https://m.youpin.mi.com/lasagne/page/5'
def getGoodList():
    res = get(url,verify=False)
    all = res['floors']
    now = []
    nowMain = all[0]['data']['result']['goods_list']
    for good1 in nowMain:
        now.append(good1)
    nowOther = all[1]['data']['result']['goods_list']
    for good2 in nowOther:
        now.append(good2)
    return _toString(now)


def _toString(goodsList):
  result = '今日小米优品共{}款众筹产品:\n\n'.format(len(goodsList))
  for good in goodsList:
      result+='名称:'+good['name']+'\n'
      result+='描述:'+good['summary']+'\n'
      result+='价格:{}\n'.format(good['price_min']/100)
      result+='图片:'+good['img_square']+'\n'
      result+='人数:{}\n'.format(good['saled'])
      result+='剩余:{}天\n'.format((datetime.fromtimestamp(good['cf_end'])-datetime.now()).days)
      result+='\n'
  return result

        


if __name__ == "__main__":
    getGoodList()