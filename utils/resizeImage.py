# -*- coding:utf-8 -*-
#图片压缩 添加水印

import PIL.Image as image


class CImageSizeHandle(object):
    def __init__(self):
        pass

    def resizeImg(self, **args):
        args_key = {'ori_img':'', 'dst_img':'', 'dst_w':'', 'dst_h':'', 'save_q':75}
        arg = {}
        for key in args_key:
            if key in args:
                arg[key] = args[key]
        im = image.open(arg['ori_img'])
        ori_w,ori_h = im.size
        widthRatio = heightRatio = None
        ratio = 1
        if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
            if arg['dst_w'] and ori_w > arg['dst_w']:
                widthRatio = float(arg['dst_w']) / ori_w #正确获取小数的方式
            if arg['dst_h'] and ori_h > arg['dst_h']:
                heightRatio = float(arg['dst_h']) / ori_h
            if widthRatio and heightRatio:
                if widthRatio < heightRatio:
                    ratio = widthRatio
                else:
                    ratio = heightRatio
            if widthRatio and not heightRatio:
                ratio = widthRatio
            if heightRatio and not widthRatio:
                ratio = heightRatio
            newWidth = int(ori_w * ratio)
            newHeight = int(ori_h * ratio)
        else:
            newWidth = ori_w
            newHeight = ori_h
        im.resize((newWidth,newHeight),image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])

    def clipResizeImg(self, **args):
        args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
        arg = {}
        for key in args_key:
            if key in args:
                arg[key] = args[key]
        im = image.open(arg['ori_img'])
        ori_w,ori_h = im.size
        dst_scale = float(arg['dst_h']) / arg['dst_w'] #目标高宽比
        ori_scale = float(ori_h) / ori_w #原高宽比
        if ori_scale >= dst_scale:
            width = ori_w
            height = int(width*dst_scale)
            x = 0
            y = (ori_h - height) / 3
        else:
            height = ori_h
            width = int(height*dst_scale)
            x = (ori_w - width) / 2
            y = 0
        box = (x,y,width+x,height+y)
        newIm = im.crop(box)
        im = None
        ratio = float(arg['dst_w']) / width
        newWidth = int(width * ratio)
        newHeight = int(height * ratio)
        newIm.resize((newWidth,newHeight),image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])

    def waterMark(self, **args):
        args_key = {'ori_img':'','dst_img':'','mark_img':'','water_opt':''}
        arg = {}
        for key in args_key:
            if key in args:
                arg[key] = args[key]
        im = image.open(arg['ori_img'])
        ori_w,ori_h = im.size
        mark_im = image.open(arg['mark_img'])
        mark_w,mark_h = mark_im.size
        option ={'leftup':(0,0),'rightup':(ori_w-mark_w,0),'leftlow':(0,ori_h-mark_h),
                 'rightlow':(ori_w-mark_w,ori_h-mark_h)
                 }
        im.paste(mark_im,option[arg['water_opt']],mark_im.convert('RGBA'))
        im.save(arg['dst_img'])
        
    def compress(self, width, height, src, dest):
        q = 35
        self.resizeImg(ori_img=src,dst_img=dest,dst_w=width,dst_h=height,save_q=q)


if __name__ == "__main__":
    handler = CImageSizeHandle()
    handler.waterMark(ori_img="test.jpg",dst_img="test2.jpg",mark_img="2.png",water_opt='rightup')
    # handler.compress(1024, 1024, "test.jpg", "test2.jpg")
