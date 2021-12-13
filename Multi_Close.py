# -*- coding: utf-8 -*
'''
cron: 15 2 * * * wskey.py
new Env('wskey转换');
'''

import asyncio,time,threading
import socket
import base64
import http.client
import json
import os
import sys
import requests

import logging
import time
from utils.config import get_config

import schedule
from main import JDMemberCloseAccount



logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

sv = ''
st = ''
uuid = ''
sign = ''



wskeylist = []





def cloud_info():
    url = str(base64.b64decode('aHR0cDovLzE1MC4xNTguMTUzLjUzOjg0NDMvY2hlY2tfYXBp').decode())
    for i in range(3):
        try:
            headers = {
                "authorization": "Bearer Shizuku",
                "Connection": "close"
            }
            res = requests.get(url=url, verify=False, headers=headers, timeout=20).text
        except requests.exceptions.ConnectTimeout:
            logger.info("\n获取云端参数超时, 正在重试!" + str(i))
        except requests.exceptions.ReadTimeout:
            logger.info("\n获取云端参数超时, 正在重试!" + str(i))
        except Exception as err:
            logger.info(str(err) + "\n未知错误云端, 退出脚本!")
            sys.exit(1)
        else:
            try:
                c_info = json.loads(res)
            except:
                logger.info("云端参数解析失败")
                sys.exit(1)
            else:
                return c_info


# 返回值 svv, stt, suid, jign
def get_sign():
    url = 'https://hellodns.coding.net/p/sign/d/jsign/git/raw/master/sign'
    res = requests.get(url=url, verify=False, timeout=20)
    sign_list = json.loads(res.text)
    svv = sign_list['sv']
    stt = sign_list['st']
    suid = sign_list['uuid']
    jign = sign_list['sign']
    return svv, stt, suid, jign








# 返回值 bool jd_ck
def appjmp(wskey, tokenKey):
    headers = {
        'User-Agent': 'okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1440x3007;os/11;network/wifi;',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    }
    params = {
        'tokenKey': tokenKey,
        'to': 'https://plogin.m.jd.com/cgi-bin/m/thirdapp_auth_page?token=AAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg',
        'client_type': 'android',
        'appid': 879,
        'appup_type': 1,
    }
    url = 'https://un.m.jd.com/cgi-bin/app/appjmp'
    try:
        res = requests.get(url=url, headers=headers, params=params, verify=False, allow_redirects=False, timeout=20)
        res_set = res.cookies.get_dict()
        pt_key = 'pt_key=' + res_set['pt_key']
        pt_pin = 'pt_pin=' + res_set['pt_pin']
        jd_ck = str(pt_key) + ';' + str(pt_pin) + ';'
        wskey = wskey.split(";")[0]
        if 'fake' in pt_key:
            logger.info(str(wskey) + ";WsKey状态失效\n")
            return False, jd_ck
        else:
            logger.info(str(wskey) + ";WsKey状态正常\n")
            return True, jd_ck
    except:
        logger.info("JD接口转换失败, 默认WsKey失效\n")
        wskey = "pt_" + str(wskey.split(";")[0])
        return False, wskey


def boom():
    url = 'https://hellodns.coding.net/p/sign/d/jsign/git/raw/master/boom'
    res = requests.get(url=url, verify=False, timeout=60)
    ex = int(res.text)
    if ex != 0:
        print("Check Failure")
        print("--------------------\n")
        sys.exit(0)
    else:
        print("Verification passed")
        print("--------------------\n")


def getToken(wskey):

    global sv, st, uuid, sign

    headers = {'cookie': wskey,
               'User-Agent': 'okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1440x3007;os/11;network/wifi;',
               'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'charset': 'UTF-8',
               'accept-encoding': 'br,gzip,deflate'}
    params = {'functionId': 'genToken', 'clientVersion': '10.1.2', 'client': 'android', 'uuid': uuid, 'st': st,
              'sign': sign, 'sv': sv}
    url = 'https://api.m.jd.com/client.action'
    data = 'body=%7B%22action%22%3A%22to%22%2C%22to%22%3A%22https%253A%252F%252Fplogin.m.jd.com%252Fcgi-bin%252Fm%252Fthirdapp_auth_page%253Ftoken%253DAAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg%2526client_type%253Dandroid%2526appid%253D879%2526appup_type%253D1%22%7D&'
    res = requests.post(url=url, params=params, headers=headers, data=data, verify=False)
    res_json = json.loads(res.text)
    tokenKey = res_json['tokenKey']
    return appjmp(wskey, tokenKey)


def appjmp(wskey, tokenKey):
    headers = {
        'User-Agent': 'okhttp/3.12.1;jdmall;android;version/10.1.2;build/89743;screen/1440x3007;os/11;network/wifi;',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', }
    params = {'tokenKey': tokenKey,
              'to': 'https://plogin.m.jd.com/cgi-bin/m/thirdapp_auth_page?token=AAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg',
              'client_type': 'android', 'appid': 879, 'appup_type': 1, }
    url = 'https://un.m.jd.com/cgi-bin/app/appjmp'
    res = requests.get(url=url, headers=headers, params=params, verify=False, allow_redirects=False)
    res_set = res.cookies.get_dict()
    pt_key = 'pt_key=' + res_set['pt_key']
    pt_pin = 'pt_pin=' + res_set['pt_pin']
    jd_ck = str(pt_key) + ';' + str(pt_pin) + ';'
    wskey = wskey.split(";")[0]
    if 'fake' in pt_key:
        print(wskey, "wskey状态失效\n")
        return False, jd_ck
    else:
        print(wskey, "wskey状态正常\n")
        return True, jd_ck


def changeck(ck):
    with open("./config.yaml","r",encoding='UTF-8') as f:

        res_str = ''
        for line in f.readlines():
            if 'cookie:' in line:
                line = 'cookie: "' + ck + '"\n'
            res_str += line

    f = open("./config.yaml","w",encoding='UTF-8')
    f.write(res_str)
    f.close()

def loadWskeyConfig(wsk_config):
    list = wsk_config.split("@")
    wskeylist = []
    portlist = []

    try:
        for item in list:
            wskeylist.append(item.split("|")[0])
            portlist.append(item.split("|")[1])
    except Exception as e:
        print("解析Wskey参数错误：" + e.args)
    return wskeylist, portlist


def runByPort(wskeylist, port):
    wskeys = wskeylist.split("&")
    for key in wskeys:
        wspin = key.split(";")[0]
        print("转化wskey:" + wspin + "\n")
        return_ws = getToken(key)
        if return_ws[0]:
            changeck(return_ws[1])
            JDMemberCloseAccount(int(port)).main()



def wskeyrun(i = 0):
    global sv, st, uuid, sign


    # if i == 0:
    #     timenow = time.localtime()
    #     if timenow.tm_mday not in [1,6,11,16,21,26]:
    #         return

    multi_enable = get_config()["multi"]["multi"]
    wskeystring = get_config()["multi"]["wskey"]

    boom()
    sv, st, uuid, sign = get_sign()

    if not multi_enable:
        JDMemberCloseAccount().main()
        return

    wskeylist, portlist = loadWskeyConfig(wskeystring)

    for i in range(len(portlist)):
        threading.Thread(target=runByPort, args= (wskeylist[i], portlist[i])).start()
        time.sleep(len(wskeylist[i].split("&")) * 3) # 根据单个端口包含的swkey数量确认延时时间，保证修改config文件时不会冲突混乱



if __name__ == '__main__':
    cookie_all = []

    print("\n开启自动退会功能\n")

    # 是否立即执行
    wskeyrun(1)


    try:
        if sys.argv[1]:
            print("强制执行一次")
            wskeyrun(1)
    except:
        pass


    schedule.every().day.at('10:00').do(wskeyrun)
    while True:
        schedule.run_pending()

