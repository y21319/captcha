#!/usr/local/python3
#-*- encoding:utf-8 -*-

from PIL import Image
import pytesseract
from aip import AipOcr
from aip import AipImageClassify

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

if __name__ == "__main__":
    # vcode = pytesseract.image_to_string('E://1.jpeg', "chi_sim")
    # print(vcode)

    """ 你的 APPID AK SK """
    APP_ID = '16972795'
    API_KEY = 'B8MfD1ItFYDrBuT5vcFnn5Rh'
    SECRET_KEY = 'AYTHKpNTdYorHGXgRZeEKOaHxEVuDIBA'
    
    image = get_file_content('E://1.jpeg')

    # client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # """ 调用通用文字识别, 图片参数为本地图片 """
    # client.basicGeneral(image);

    # """ 如果有可选参数 """
    # options = {}
    # options["language_type"] = "CHN_ENG"
    # options["detect_direction"] = "true"
    # options["detect_language"] = "true"
    # options["probability"] = "true"

    # """ 带参数调用通用文字识别, 图片参数为本地图片 """
    # result = client.basicGeneral(image, options)
    # print(result)

    # url = "http//www.x.com/sample.jpg"

    # """ 调用通用文字识别, 图片参数为远程url图片 """
    # client.basicGeneralUrl(url);

    # """ 如果有可选参数 """
    # options = {}
    # options["language_type"] = "CHN_ENG"
    # options["detect_direction"] = "true"
    # options["detect_language"] = "true"
    # options["probability"] = "true"

    # """ 带参数调用通用文字识别, 图片参数为远程url图片 """
    # client.basicGeneralUrl(url, options)

    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
    """ 如果有可选参数 """
    options = {}
    options["baike_num"] = 9

    """ 带参数调用通用物体识别 """
    result = client.advancedGeneral(image, options)
    print(result)