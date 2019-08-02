#!/usr/local/python
#-*- encoding:utf-8 -*-

import requests
import time
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

def download(url,path,ext,count=50):
    if not os.path.exists(path):
        os.makedirs(path)

    for i in range(count):
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            with open(path+str(i)+ext, 'wb+') as f:
                f.write(response.content)
                f.close()
        time.sleep(3)