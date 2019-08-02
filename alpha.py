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

if __name__ == "__main__":
    #下载验证码
    # get.download('https://gitee.com/rucaptcha?1564734861478','D://captcha//oschina//','.gif',50)
