# -*- coding:utf-8 -*-
#图片压缩
from PIL import Image,ImageEnhance,ImageFilter
import cv2

########################自定义图像压缩函数############################
def imgZip(imagePath,newName=None):
    if newName is None:
       temp = imagePath.split('.')
       newName = temp[0]+'_small.'+temp[1]
    image = cv2.imread(imagePath)
    res = cv2.resize(image, (1280, 960), interpolation=cv2.INTER_AREA)
    cv2.imwrite(newName, res)
    imgE = Image.open(newName)
    imgEH = ImageEnhance.Contrast(imgE)
    img1 = imgEH.enhance(2.8)
    gray1 = img1.convert("L")
    gary2 = gray1.filter(ImageFilter.DETAIL)
    gary3 = gary2.point(lambda i: i * 0.9)
    gary3.save(newName)
    return newName

if __name__ == '__main__':
   imgZip('3.png')