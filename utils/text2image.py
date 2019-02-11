# -*- coding:utf-8 -*-
#txt转img

import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import shutil

defaultConfig = {
    "maxLen": 150,
    "fontSize": 15,
    "fontColor": "#000",
    "fontBackgroundColor": "#fff",
    "fontType": os.path.join(os.getcwd(), "asset", "fonts", "simsun.ttf"),
}


class DrawText:
    def __init__(self, config={}):
        self.gap = 10  # 预留的边距
        self.picture_sieze = (0, 0)
        self.font_size = int(config["fontSize"] if 'fontSize' in
                             config else defaultConfig["fontSize"])
        self.font_source = str(config["fontType"] if 'fontType' in
                               config else defaultConfig["fontType"])
        self.font_color = str(config["fontColor"] if 'fontColor' in
                              config else defaultConfig["fontColor"])
        self.row_max_len = int(config["maxLen"] if 'maxLen' in
                               config else defaultConfig["maxLen"])
        self.font_background_color = str(
            config["fontBackgroundColor"] if 'fontBackgroundColor' in
            config else defaultConfig["fontBackgroundColor"])
        self.font = ImageFont.truetype(self.font_source, self.font_size)

    def draw_text(self, text, path):
        try:
            row = int(len(text) / self.row_max_len)  # 先计算出文字有几行
            if len(text) % self.row_max_len > 0:
                row += 1

            # 创建图片空间
            width = int(self.row_max_len * (self.font_size * 0.54) +
                        self.gap * 2)
            height = int(row * (self.font_size + self.gap) + self.gap)
            img = Image.new('RGB', (width, height), self.font_background_color)
            draw = ImageDraw.Draw(img)

            # 在图片空间上写字
            for index in range(0, row):
                draw.text(
                    (self.gap, index * (self.font_size + self.gap) + self.gap),
                    text[index * self.row_max_len:(index + 1) *
                         self.row_max_len],
                    font=self.font,
                    fill=self.font_color)
            img.save(path)
            # img.convert("RGB").save(path, "BMP")
            return width, height
        except Exception as error_message:
            print(str(error_message))

    def draw_file(self, filePath, imgPath):
        try:
            file = open(filePath)
            tempPath = 'temp/images/'
            if os.path.exists(tempPath):
                shutil.rmtree(tempPath)
            os.mkdir(tempPath)
            count = 0
            sizes = []
            for line in file:
                count += 1
                width, height = self.draw_text(
                    line, '{}{}.png'.format(tempPath, count))
                sizes.append([width, height])
            file.close()
            imghigh = 0
            imgwidth = 0
            for index, size in enumerate(sizes):
                width = size[0]
                height = size[1]
                if width > imgwidth:
                    imgwidth = width
                if index != len(sizes) - 1:
                    imghigh += height
            imagefile = []
            for _, _, files in os.walk(tempPath):
                for i in range(1, len(files)):
                    imagefile.append(Image.open(tempPath + '{}.png'.format(i)))
            target = Image.new('RGB', (imgwidth, imghigh))  #最终拼接的图像的大小
            top = 0
            for index, image in enumerate(imagefile):
                target.paste(image, (0, top))
                top += sizes[index][1]  #从上往下拼接，左上角的纵坐标递增
                target.save(imgPath, quality=100)
            shutil.rmtree(tempPath)
        except Exception as error_message:
            print(str(error_message))


def text2Image(text, path=None):
    if path is None:
        path = 'temp/{}.png'.format(text[:5])
    DrawText().draw_text(text, path)


def textFile2Image(filePath, path=None):
    # lines = len([ "" for line in open(logName,"r")])
    if path is None:
        temp = filePath.split('/')
        path = 'temp/{}.png'.format(temp[-1].split('.')[0])
    DrawText().draw_file(filePath, path)
