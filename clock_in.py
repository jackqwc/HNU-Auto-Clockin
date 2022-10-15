import requests
import json
import argparse
import re
import cv2
import numpy as np
import math
import random
import hashlib
import time
import base64
from pyDes import des, PAD_PKCS5, CBC
from captcha import recognize

# 初始化变量
parser = argparse.ArgumentParser()
parser.add_argument('--username', type=str, default=None)
parser.add_argument('--password', type=str, default=None)
parser.add_argument('--province', type=str, default=None)
parser.add_argument('--city', type=str, default=None)
parser.add_argument('--county', type=str, default=None)
args = parser.parse_args()

def captchaOCR():
    captcha = ''
    token   = '' 
    while len(captcha) != 4:
        token = requests.get('https://fangkong.hnu.edu.cn/api/v1/account/getimgvcode').json()['data']['Token']
        image_raw = requests.get(f'https://fangkong.hnu.edu.cn/imagevcode?token={token}').content
        image = cv2.imdecode(np.frombuffer(image_raw, np.uint8), cv2.IMREAD_COLOR)
        try:
            captcha = recognize(image)
        except Exception as err:
            print(err)

    return token, captcha

def timestamp():
    return str(int(time.time() * 1000))

def desEncrypt(str):
    DesObj = des('hnu88888', CBC, 'hnu88888', padmode=PAD_PKCS5)
    return base64.b64encode(DesObj.encrypt(str)).decode('utf-8')

def signMD5():
    md = hashlib.md5()
    md.update(f"{timestamp()}|{nonce}|hnu123456".encode('utf-8'))
    return str(md.hexdigest())

def nonce():
    return str(math.ceil(9999999*random.random()))

def login():
    login_url = 'https://fangkong.hnu.edu.cn/api/v1/account/login'
    token, captcha = captchaOCR()
    login_info = {"nonce":nonce(),"sign":signMD5(),"timestamp":timestamp(),"Code":desEncrypt(args.username),"Password":desEncrypt(args.password),"WechatUserinfoCode":"null","VerCode":captcha,"Token":token}
    loggingin = requests.post(login_url, json=login_info)
    set_cookie = loggingin.headers['Set-Cookie']
    access_token = json.loads(loggingin.text)['data']['AccessToken']
    regex = r"\.ASPXAUTH=(.*?);"
    ASPXAUTH = re.findall(regex, set_cookie)[2]

    headers = {'Cookie': f'.ASPXAUTH={ASPXAUTH}; TOKEN={access_token}'}
    return headers

def setLocation():
    real_address = "湖南大学天马学生公寓" # 在此填写详细地址
    return real_address

def main():
    clockin_url = 'https://fangkong.hnu.edu.cn/api/v1/clockinlog/add'
    headers = login()
    real_address = setLocation()
    clockin_data = {
                    "nonce":nonce(),
                    "sign":signMD5(),
                    "timestamp":timestamp(),
                    "Longitude":"null",
                    "Latitude":"null",
                    "RealProvince":args.province,
                    "RealCity":args.city,
                    "RealCounty":args.county,
                    "RealAddress":real_address,
                    "BackState":1,
                    "MorningTemp":"36.5",
                    "NightTemp":"36.5",
                    "tripinfolist":[],
                    "QRCodeColor":"绿色"
                    }

    clockin = requests.post(clockin_url, headers=headers, json=clockin_data)

    if clockin.status_code == 200:
        if '成功' in clockin.text or '已提交' in clockin.text:
            isSucccess = 0
        else:
            isSucccess = 1
            print(json.loads(clockin.text)['msg'])
    else:
        isSucccess = 1
    print(json.loads(clockin.text)['msg'])

    return isSucccess

main()

# for i in range(10):
#     try:    
#         a = main()
#         if a == 0:
#             break
#         elif i == 9 and a == 1:
#             raise ValueError("打卡失败")
#         else:
#             continue
#     except:
#         continue
