#!/usr/local/python3
# -*- encoding:utf-8 -*-

'''
    复杂的字母和数字有干扰线的需要使用sklearn训练模型之后进行识别
    https://gitee.com/rucaptcha?1564734861478
    https://www.oschina.net/action/user/captcha?t=0.4158515568319441
'''

import numpy as np
from sklearn import neighbors
import os
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import cv2
import get
from PIL import Image

def binarize(img,threshold):
    img = img.convert('L')
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x,y] < threshold:
                pixdata[x,y] = 0
            else:
                pixdata[x,y] = 255
    return img

#切割图片
def cut_img(img):
    region = img.crop((20, 20, 200, 70))
    return region

#获取所有图片进行切割
def split_img():
    for root, dirs, files in os.walk('D://captcha//oschina//'):
        for file in files:
            # 对于一些彩色的验证码需要做裁剪边缘，以及二值化和灰度化处理，而一些本身就是黑色的验证码就不需要处理
            # p = Image.open('D://captcha//oschina//%s' % file)
            # p = cut_img(p)
            b = binarize(p,170)
            break

if __name__ == "__main__":
    #下载验证码
    # get.download('https://gitee.com/rucaptcha?1564734861478','D://captcha//oschina//','.gif',50)
    #分割验证码
    split_img()
