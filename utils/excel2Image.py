# -*- coding:utf-8 -*-
#excel表格转换为图片

import pandas as pd
import codecs
import imgkit
import os,shutil
 
 
# ReportImage -> report convert include multiple sheets into pictures
class ReportImage:
 
    def __init__(self):
        pass
 
    # excel_html -> convert excel include multiple sheets into multiple html file
    # excel_file -> file
    # html_path  -> path
    @staticmethod
    def excel2Html(excel_file, html_path):
        html_list = []
        excel_obj = pd.ExcelFile(excel_file)
        sheet_list = excel_obj.sheet_names
        index = 0
        for i in sheet_list:
            html_file = html_path + i + ".html"
            excel_data = excel_obj.parse(excel_obj.sheet_names[index])
            with codecs.open(html_file, 'w', 'utf-8') as html:
                html.write(excel_data.to_html(header=True, index=True))
            html_list.append(html_file)
            index += 1
        return html_list
 
    # html_image -> convert htmls into pictures file
    # html_list  -> list
    # image_path -> path
    @staticmethod
    def html2Image(html_list, image_path,quality=94):
        image_list = []
        index = 0
        for i in html_list:
            img_obj = image_path + str(index) + ".png"
            with open(i, 'r') as html_file:
                imgkit.from_file(html_file, img_obj, options={"encoding":"UTF-8","quality":quality})
            index += 1
            image_list.append(img_obj)
        return image_list
 
    @staticmethod
    def excel2Image(excelFilePath, imageDirPath,quality=94):
        if not os.path.exists(imageDirPath):
           os.mkdir(imageDirPath)
        htmlList = ReportImage.excel2Html(excelFilePath,imageDirPath)
        imageList = ReportImage.html2Image(htmlList, imageDirPath,quality)
        print('转换',excelFilePath,'完毕')
        return imageList

 
if __name__ == '__main__':
    dir = 'ttt/'
    print(ReportImage.excel2Image('test.xlsx',dir,100))
    # shutil.rmtree(dir) 
