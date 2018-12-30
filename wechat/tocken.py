# -*- coding: utf-8 -*-
# 获取AccessToken

import time,json
from fetch import get,post

class Tocken:    
  def __init__(self):        
    self.__accessToken = ''        
    self.__leftTime = 0    
  def __real_get_access_token(self):        
    appId = "wxed7b342c476bed4f"        
    appSecret = "09c52bbb765bd63ece6b964e3091f960"        
    postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="  
    "client_credential&appid=%s&secret=%s" % (appId, appSecret))    
    urlResp = get(postUrl)        
    self.__accessToken = urlResp['access_token']        
    self.__leftTime = urlResp['expires_in']    
  def get_access_token(self):        
    if self.__leftTime < 10:            
      self.__real_get_access_token()        
      return self.__accessToken    
  def run(self):        
    while(True):            
      if self.__leftTime > 10:                
        time.sleep(2)                
        self.__leftTime -= 2            
      else:                
        self.__real_get_access_token()
  
if __name__ == '__main__':
   token = Tocken().get_access_token()
   print(token)