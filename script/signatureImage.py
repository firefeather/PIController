
import os
import matplotlib.pyplot as plt
import random
from wordcloud import WordCloud,ImageColorGenerator
import sys
from time import time
import re
from scipy.misc import imread

BACKGROUND_IMGS = [imread('./image/1.png'),imread('./image/2.jpeg'),imread('./image/3.jpg'),imread('./image/4.jpg'),imread('./image/5.png'),imread('./image/6.jpg'),None]

def getPath():
    path = "./Signature/"
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def getSignatures(fileName):
  # 获取词云
    friends = getFriendsInfo()
    file = open(fileName, 'a', encoding='utf-8')
    for f in friends:
        signature = f["Signature"].strip().replace("emoji", "").replace("span", "").replace("class", "")
        rec = re.compile("1f\d+\w*|[<>/=]")
        signature = rec.sub("", signature)
        file.write(signature + "\n")

# 生成词云图
def createWordCloud():
    # 读取文件内容
    fileName = (getPath()+'signature{}').format(int(time()))
    txtName = fileName+'.txt'
    getSignatures(txtName)
    text = open(txtName, encoding='utf-8').read()
    
    # 注释部分采用结巴分词
    # wordlist = jieba.cut(text, cut_all=True)
    # wl = " ".join(wordlist)
    
    # 设置词云
    background = random.choice(BACKGROUND_IMGS)
    #改变字体颜色
    if background is None:
       img_colors = None
    else:
       img_colors = random.choice((None,ImageColorGenerator(background))) 

    #字体颜色为背景图片的颜色
    wc = WordCloud(
        # 设置背景颜色
        background_color="white",
        # 设置最大显示的词云数
        max_words=2000,
        # 这种字体都在电脑字体中，window在C:\Windows\Fonts\下，mac下可选/System/Library/Fonts/PingFang.ttc 字体
        font_path='/System/Library/Fonts/PingFang.ttc',
        # height=500,
        # width=500,
        # 设置字体最大值
        # max_font_size=60,
        # 设置有多少种随机生成状态，即有多少种配色方案
        # random_state=30,
        mask = background,
        color_func=img_colors
        )
    
    myword = wc.generate(text)  # 生成词云 如果用结巴分词的话，使用wl 取代 text， 生成词云图
    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    # plt.show()
    imgName = fileName+'.png'
    wc.to_file(imgName)  # 把词云保存下
    os.remove(txtName)
    if os.path.exists(imgName):
        try:
            return "@img@{}".format(imgName)
        except BaseException as e:
            import traceback
            traceback.print_exc()
            return "生成词云图失败，请重试。"
    else:
        return "生成失败，请重试。"
