import os, sys
import subprocess
import requests
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import time


def excuteCommand(com):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    print("cmd in:", com)
    print("cmd out: ", out.decode())
    return out.decode()


def download(link, file_name):
    response = requests.get(link)
    file = response.content
    with open(file_name, 'wb') as f:
        f.write(file)


# 进度条模块
def progressbar(url, path):
    if not os.path.exists(path):  # 看是否有该文件夹，没有则创建文件夹
        os.mkdir(path)
    start = time.time()  # 下载开始时间
    response = requests.get(url, stream=True)  # stream=True必须写上
    size = 0  # 初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    try:
        if response.status_code == 200:  # 判断是否响应成功
            print('Start download,[File size]:{size:.2f} MB'.format(
                size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
            filepath = path + "/" + url.split('/')[-1]  # 设置图片name，注：必须加上扩展名
            with open(filepath, 'wb') as file:  # 显示进度条
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    print('\r' + '[下载进度]:%s%.2f%%' % (
                    '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')
        end = time.time()  # 下载结束时间
        print('Download completed!,times: %.2f秒' % (end - start))  # 输出下载用时时间
    except Exception as e:
        print(str(e))


def installPython():
    url = "https://www.python.org/ftp/python/3.7.0/python-3.7.0-amd64.exe"
    progressbar(url, ".")
    excuteCommand(url.split("/")[-1] + " InstallAllUsers=1 PrependPath=1")
    os.remove(url.split("/")[-1])



if __name__ == '__main__':
    installPython()