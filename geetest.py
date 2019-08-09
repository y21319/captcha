#!/usr/local/python3
# -*- encoding:utf-8 -*-

'''
    极验拖拽验证码破解
'''

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import base64

from PIL import Image
from selenium.webdriver import ActionChains
import os

import random
THRESOLD = 60

class CrackGeetest:
    
    #初始化
    def __init__(self, url, usernamei, passwordi, submit, submittype,userinfo, acc, pwd):
        self.url = url
        self.usernamei = usernamei
        self.passwordi = passwordi
        self.submit = submit
        self.userinfo = userinfo
        self.submittype = submittype
        options = webdriver.ChromeOptions()
        options.add_argument('User-Agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36')
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 20)
        self.account = acc
        self.password = pwd
        self.browser.get(self.url)

    #获取验证码按钮
    def get_geetest_btn(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_radar_tip')))
        return button

    #获取用户名密码
    def get_username_passwod(self):
        username = self.wait.until(EC.presence_of_element_located((By.ID,self.usernamei)))
        password = self.wait.until(EC.presence_of_element_located((By.ID,self.passwordi)))
        return username,password
    
    #获取登录提交按钮
    def get_submit(self):
        if self.submittype == 'class':
            button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,self.submit)))
        elif self.submittype == 'id':
            button = self.wait.until(EC.element_to_be_clickable((By.ID,self.submit)))
        else:
            button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,self.submit)))
        return button
    
    def get_code_image(self,cls):
        js = 'return document.getElementsByClassName("'+cls+'")[0].toDataURL("image/png")'
        image = self.browser.execute_script(js)
        imagebase64 = image.split(',')[1]
        imagebytes = base64.b64decode(imagebase64)
        with open('/Users/yuanxiao/Downloads/'+cls+'.png','wb') as f:
            f.write(imagebytes)
        return '/Users/yuanxiao/Downloads/'+cls+'.png'

    #比较两张图片之间的像素点差异,比较rgb之间的差异
    def equal(self,fullimage,someimage,x,y):
        pix1 = fullimage.load()[x,y]
        pix2 = someimage.load()[x,y]
        if abs(pix1[0] - pix2[0]) < THRESOLD and abs(pix1[1] - pix2[1]) < THRESOLD and abs(pix1[2] - pix2[2]) < THRESOLD:
            return True
        else:
            return False

    #获取两张图片的差异像素开始点的left
    def differ_code(self,fullimagepath,someimagepath,sideimagepath):
        fullimage = Image.open(fullimagepath)
        someimage = Image.open(someimagepath)
        for x in range(fullimage.size[0]):
            for y in range(fullimage.size[1]):
                if not self.equal(fullimage,someimage,x,y):
                    return x - self.get_side_left(sideimagepath,x)
        return 0
    
    #获取滑块左侧边距
    def get_side_left(self,sideimagepath,left):
        sideimage = Image.open(sideimagepath)
        for x in range(left,sideimage.size[0]):
            for y in range(sideimage.size[1]):
                pix = sideimage.load()[x,y]
                if pix[3] > 0:
                    return x
        return 0

    def get_codes(self):
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_window')))
        fullimage = self.get_code_image('geetest_canvas_fullbg')
        someimage = self.get_code_image('geetest_canvas_bg')
        sideimage = self.get_code_image('geetest_canvas_slice')
        try:
            return self.differ_code(fullimage,someimage,sideimage)
        finally:
            os.remove(fullimage)
            os.remove(someimage)
            os.remove(sideimage)

    #获取拖动滑块轨迹，模拟你为拖动效果
    def get_track(self,distance):
        tarck = []
        if distance < 10:
            tarck.append(distance)
            return tarck
        current = 0
        mid = distance * 4 / 5
        t = 0.2
        v = 0
        while current < distance:
            if current < mid:
                a = 100
            else:
                a = 80
            v0 = v
            v = v0 + a * t
            move = v0 * t + 0.5 * a * pow(t,2)
            current += move
            if current < distance:
                tarck.append(move)
            else:
                tarck.append(distance - current + move)
        tarck.extend(self.randomsuffix())
        return tarck

    #轨迹扰乱
    def randomsuffix(self):
        result = random.randint(0,1)
        return self.randomtarcks(result)

    #随机路径
    def randomtarcks(self,direction):
        tracks = []
        if direction == 0:
            total = random.uniform(0,5)
        else:        
            total = random.uniform(-5,0)
        count = random.randint(2,4)
        tracks.extend([total / count] * count)
        tracks.extend([-total / count] * count)
        return tracks

    #获取滑块
    def get_slider(self):
        slider = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_slider_button')))
        return slider

    #模拟滑块动画
    def move_action(self,slider,tracks):
        #需要重新控制大小否则无法成功破解
        self.browser.execute_script('document.getElementsByClassName("geetest_widget")[0].style.cssText="width:100%;margin:0;";document.getElementsByClassName("geetest_wrap")[0].style.cssText="padding:0;";')
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x,yoffset=0).perform()
        ActionChains(self.browser).release().perform()

    def login(self):
        username,password = gc.get_username_passwod()
        username.click()
        username.clear()
        username.send_keys(gc.account+'1')
        password.click()
        password.clear()
        password.send_keys(gc.password+'1')
        gc.get_submit().click()
        left = gc.get_codes()
        gc.move_action(gc.get_slider(), gc.get_track(left))
        # username.clear()
        # username.send_keys(gc.account)
        # password.clear()
        # password.send_keys(gc.password)
        userinfo = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,self.userinfo)))
        print(userinfo.get_attribute('class'))

if __name__ == "__main__":
    # gc = CrackGeetest(r'https://passport.bilibili.com/login',r'login-username',r'login-passwd',r'btn-login',r'class',r'nav-con',r'******',r'******')
    gc = CrackGeetest(r'http://www.gsxt.gov.cn/index.html',r'keyword',r'keyword',r'btn_query',r'id',r'main-layout',r'中国石油',r'中国石油')
    gc.login()


