# -*- coding: utf-8 -*-
# 所有用户  用于权限控制

import pickle,os
from user import User
from config import getManagerInfo

USERS_FILE_PATH = './USERS.DB'
global ALL_USERS
ALL_USERS = None


def initManager():
    managerInfo = getManagerInfo()
    managerInfo['level'] = 10
    return User(**managerInfo)

MANAGER = initManager()

def loadUsersFromDisk():
    global ALL_USERS
    try:
       with open(USERS_FILE_PATH, 'rb') as f:# load 从数据文件中读取数据，并转换为python的数据结构
            ALL_USERS = pickle.load(f) or []
    except Exception: #捕获异常
       print('读取缓存文件失败')
       ALL_USERS = []
    # print "加载用户列表",ALL_USERS

def saveUsers():
    global ALL_USERS
    print ("存储用户列表",ALL_USERS)
    with open(USERS_FILE_PATH, 'wb') as f: # dump 将数据通过特殊的形式转换为只有python语言认识的字符串，并写入文件
         pickle.dump(ALL_USERS, f)

def updateUserByDict(userInfo):
    global ALL_USERS
    if 'openid' in userInfo:
       userId = userInfo['openid']
    elif 'id' in userInfo:
        userId = userInfo['id']
    if userId is None:
       print('updateUserByDict失败','无用户id')
       return '更新失败'
    users = findUser(id = userId)
    if len(users) == 0:
       return '未找到用户,更新失败'
    user = users[0]
    if 'nickname' in userInfo:
        user.Name = userInfo['nickname']
    if 'name' in userInfo:
        user.Name = userInfo['name']
    if 'subscribe_time' in userInfo:
        user.Time = userInfo['subscribe_time']
    if 'level' in userInfo:
        user.Level = userInfo['level']
    if 'phone' in userInfo:
        user.Phone = userInfo['phone']
    if 'email' in userInfo:
        user.Email = userInfo['email']
    # print "更新用户列表",users,ALL_USERS
    saveUsers()
    return '更新成功'


def removeUser(**idOrName):
    global ALL_USERS
    # print "移除用户",user,ALL_USERS
    if 'id' in idOrName:
       ALL_USERS = list(filter(lambda user:user.Id != idOrName['id'], ALL_USERS))
    if 'name' in idOrName:
       ALL_USERS = list(filter(lambda user:user.Name != idOrName['name'], ALL_USERS))
    saveUsers()

def addUser(newUser):
  global ALL_USERS
#   print ("添加用户",user,ALL_USERS)
  if ALL_USERS is None:
      loadUsersFromDisk()
  for user in ALL_USERS:
      if newUser.Id == user.Id:
         print ("已有该用户,不再添加")
         return
  ALL_USERS.append(newUser)
  saveUsers()

def getUsers():
  global ALL_USERS
  if ALL_USERS is None:
      loadUsersFromDisk()
  return ALL_USERS

def findUser(**idOrName):
    global ALL_USERS
    if ALL_USERS is None:
      loadUsersFromDisk()
    users = []
    if 'id' in idOrName:
       userId = idOrName['id']
       if userId == MANAGER.Id:
          users.append(MANAGER)
       else:  
          users = list(filter(lambda user:user.Id == userId, ALL_USERS))
    if 'name' in idOrName:
       userName = idOrName['name']
       if userName == MANAGER.Name:
          users.append(MANAGER)
       else:  
          users = list(filter(lambda user:user.Name == userName, ALL_USERS))
    return users

def findAndCreatedIfUserNotFound(**idOrName):
    userList = findUser(**idOrName)
    if len(userList) == 0:#如果没找到该用户 则将该用户保存后返回
        user = User(id=idOrName['id'])
        addUser(user)
        userList.append(user)
    return userList

if __name__ == "__main__":
    # user = User(name='333aaa')
    print(MANAGER.Id=='omyqB1uI5qSm5Ypdum43V2zMrTVk')