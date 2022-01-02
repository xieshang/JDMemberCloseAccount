# -*- coding: utf-8 -*
'''
cron: 15 2 * * * wskey.py
new Env('wskey转换');
'''
import threading
import os
import platform
import time

from PyQt5.QtCore import pyqtSignal, QThread

from utils.config import get_config
from utils.wskToCk import getToken
from main import JDMemberCloseAccount

import os
import sys
import yaml
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from JDMCA_Form import Ui_JDMCA
from utils.config import get_config
import subprocess
from utils.getchromedriver import check_driver_version

sys_type = platform.system()

mirror_dic = {
    "清华": "https://pypi.tuna.tsinghua.edu.cn/simple/",
    "豆瓣": "https://pypi.douban.com/simple/",
    "阿里": "https://mirrors.aliyun.com/pypi/simple/",
    "腾讯": "https://mirrors.cloud.tencent.com/pypi/simple"
}


def excuteCommand(com):
    # ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    # out, err = ex.communicate()
    # status = ex.wait()
    # print("cmd out: ", out.decode())
    # return out.decode()

    print("cmd in:", com)
    res = ''
    p = subprocess.Popen(com, stdout=subprocess.PIPE, bufsize=1)
    for line in iter(p.stdout.readline, b''):
        try:
            line = line.decode()
        except:
            line = str(line)
        res += line
        print(line)
    p.stdout.close()
    p.wait()
    return res


class JDMCA_Tools(QtWidgets.QWidget, Ui_JDMCA):
    def __init__(self):
        super(JDMCA_Tools, self).__init__()
        self.setupUi(self)
        self.resize(self.width(), self.height())
        self.setMaximumSize(self.width(), self.height())
        self.setMinimumSize(self.width(), self.height())
        self.form_max_height = self.height()
        self.KeyTable.setColumnWidth(0, 30)
        self.KeyTable.setColumnWidth(1, 40)
        self.KeyTable.setColumnWidth(2, 500)
        row_cnt = self.KeyTable.rowCount()
        for i in range(8):
            self.KeyTable.insertRow(row_cnt)

        self.ChkEnable = []
        for i in range(self.KeyTable.rowCount()):
            self.ChkEnable.append(QtWidgets.QTableWidgetItem())
            self.ChkEnable[i].setCheckState(QtCore.Qt.Unchecked)  # 把checkBox设为未选中状态
            self.KeyTable.setItem(i, 0, self.ChkEnable[i])  # 在(x,y)添加checkBox
            self.KeyTable.setRowHeight(i, 8)

        # 每个号的日志关联
        self.logtext = [self.LogText_1]  # 添加一个元素，方便代码自动联想
        self.logtabs = [self.tab_1]
        for i in range(self.KeyTable.rowCount()):
            self.LogTab.setTabText(i, "")
            self.LogTab.setTabVisible(i, False)
            # 将所有的logtext放到list里方便后面调用
            if i == 0:
                continue
            self.logtext.append(eval('self.LogText_' + str(i + 1)))
            self.logtabs.append(eval('self.tab_' + str(i + 1)))
            self.logtext[i].setText("")



        # self.Chk_Muilt.clicked.connect(self.Chk_Muilt_Clicked)
        self.Btn_Run.clicked.connect(self.Btn_Run_Clicked)
        self.Btn_InstallPip.clicked.connect(self.Btn_InstallPip_Clicked)
        self.Btn_unInstallPip.clicked.connect(self.Btn_unInstallPip_Clicked)
        self.Btn_InstallPip_One.clicked.connect(self.Btn_InstallPip_One_Clicked)
        self.Btn_downchromedriver.clicked.connect(self.Btn_downchromedriver_Clicked)
        self.Btn_unInstallPip_One.clicked.connect(self.Btn_unInstallPip_One_Clicked)
        self.setWindowTitle("东东退会 2022-01-02 fix")
        self.init()
        self.GetPythonCmd()

    def Btn_downchromedriver_Clicked(self):
        check_driver_version(".\drivers\chromedriver.exe")

    def Btn_unInstallPip_One_Clicked(self):
        cmd = '' + self.pipcmd + ' uninstall ' + self.Txt_ModuleName.text() + " -y"
        excuteCommand(cmd)
        res = excuteCommand(self.pipcmd + " list")
        modulename = self.Txt_ModuleName.text().split("=")[0].replace("~", "").replace(">", "").replace("<", "").upper()
        if modulename not in res:
            QMessageBox.information(self, '提示', "卸载{}成功".format(self.Txt_ModuleName.text()))

    def Btn_InstallPip_One_Clicked(self):
        cmd = '' + self.pipcmd + ' install -i ' + mirror_dic[self.Combox_mirror.currentText()] + " " + \
              self.Txt_ModuleName.text()
        excuteCommand(cmd)
        res = excuteCommand(self.pipcmd + " list")
        modulename = self.Txt_ModuleName.text().split("=")[0].replace("~", "").replace(">", "").replace("<", "").upper()
        if modulename in res.upper():
            QMessageBox.information(self, '提示', "安装{}成功".format(self.Txt_ModuleName.text()))
        else:
            if modulename.replace("_", "-") in res.upper():
                QMessageBox.information(self, '提示', "安装{}成功".format(self.Txt_ModuleName.text()))
            else:
                QMessageBox.warning(self, '提示', "依赖安装好像有问题。。。")
        pass

    def CheckModuleState(self):
        print('判断依赖安装情况')
        res = excuteCommand(self.pipcmd + " list")
        return 'opencv-python'.upper() in res.upper()

    def Btn_InstallPip_Clicked(self):
        if self.CheckModuleState():
            return

        print('升级pip')
        excuteCommand('' + self.pythoncmd + ' -m pip install --upgrade pip')
        print("选择源:" + self.Combox_mirror.currentText())

        print('判断torch')
        res = excuteCommand(self.pipcmd + ' list')
        if 'torch'.upper() not in res.upper():
            print('尝试安装torch')
            cmd = (self.pipcmd + ' install torch -f https://download.pytorch.org/whl/cu102/torch_stable.html')
            excuteCommand(cmd)
            res = excuteCommand(self.pipcmd + ' list')
            if 'torch'.upper() not in res.upper():
                QMessageBox.information(self, '提示', "torch安装失败，python是64位吗？\r\n如果不行，就把python卸了让我来安装吧！\r\n"
                                                    "卸载后记得清理一下系统环境path哦！")
                return

        cmd = ('' + self.pipcmd + ' install  -i ' + mirror_dic[self.Combox_mirror.currentText()] +
               ' requests~=2.25.1 PyYAML~=5.4.1 psutil~=5.8.0 selenium~=3.141.0 easyocr~=1.3.2 Pillow~=8.2.0 '
               'urllib3~=1.26.5 baidu-aip==2.2.18.0 websockets opencv_python~=4.5.2.54 '
               'func-timeout~=4.3.5 msedge-selenium-tools~=3.141.3 numpy~=1.19.5 apscheduler')
        excuteCommand(cmd)
        if self.CheckModuleState():
            QMessageBox.information(self, '提示', "安装opencv-python成功，其他依赖应该也OK了")
            return True
        else:
            QMessageBox.warning(self, '提示', "依赖安装好像有问题。。。")
            return False

    def Btn_unInstallPip_Clicked(self):
        cmd = ('' + self.pipcmd + ' uninstall -y opencv_python')
        res = excuteCommand(cmd)
        res = excuteCommand(self.pipcmd + " list")
        if 'opencv_python'.upper() not in res.upper():
            QMessageBox.information(self, '提示', "卸载opencv-python成功")
        else:
            QMessageBox.warning(self, '提示', "好像卸载失败了。。。")

    def Chk_Muilt_Clicked(self):
        if self.Chk_Muilt.isChecked():
            self.Chk_LocalMsg.setChecked(True)
            self.Chk_LocalMsg.setEnabled(False)
            self.Txt_Cookie.setEnabled(False)
            self.KeyTable.setEnabled(True)
        else:
            self.Chk_LocalMsg.setEnabled(True)
            self.Txt_Cookie.setEnabled(True)
            self.KeyTable.setEnabled(False)

    def init(self):
        config = yaml.safe_load(open(get_file("config.yaml"), 'r', encoding='utf-8'))
        try:
            self.Chk_Auto.setChecked(config["main"]["cron_enable"])
            self.Chk_Muilt.setChecked(config["multi"]["multi_enable"])

            row_idx = 0
            for i in range(1, 10):
                try:
                    self.KeyTable.setItem(row_idx, 1, QTableWidgetItem(str(config["multi"]["port" + str(i)])))
                    self.KeyTable.setItem(row_idx, 2, QTableWidgetItem(config["multi"]["key" + str(i)]))
                    row_idx += 1
                except Exception as e:
                    print(str(e))
        except:
            self.Chk_Auto.setEnabled(False)
            self.Chk_Muilt.setEnabled(False)
            self.KeyTable.setEnabled(False)

        self.Txt_Cookie.setPlainText(config["cookie"])
        self.Chk_LocalMsg.setChecked(1 - config["sms_captcha"]["jd_wstool"])
        self.Chk_CloudID.setChecked(config["shop"]["add_remote_shop_data"])
        self.Chk_Headless.setChecked(config["selenium"]["headless"])

        # self.Chk_Muilt_Clicked()
        pass

    def GetPythonCmd(self):
        """
        检测系统python环境
        :return:
        """
        self.pythoncmd = ''
        self.pipcmd = ''

        res = os.popen("python --version")
        res = res.read()
        if 'python 3'.upper() in res.upper():
            self.pythoncmd = 'python'
        else:
            res = os.popen("python3 --version")
            res = res.read()
            if 'python 3'.upper() in res.upper():
                self.pythoncmd = 'python3'

        res = os.popen("pip --version")
        res = res.read()
        if 'python 3'.upper() in res.upper():
            self.pipcmd = 'pip'
        else:
            res = os.popen("pip3 --version")
            res = res.read()
            if 'python 3'.upper() in res.upper():
                self.pipcmd = 'pip3'
        errmsg = ''
        errtype = 0
        if self.pythoncmd == '':
            errmsg += '请安装python3.6~3.9版本\n'
            errtype = 1
        if self.pipcmd == '' and errtype == 0:
            errmsg += '请安装pip\n'
            errtype = 2

        if errmsg != '':
            if errtype == 2:
                btn = QMessageBox.information(self, '错误', errmsg)
            else:
                btn = QMessageBox.information(self, '错误', errmsg + "是否启动自动安装python？",
                                              QMessageBox.Ok | QMessageBox.Cancel)
            if btn == QMessageBox.Ok:
                from utils.installpython import installPython
            installPython()
            QMessageBox.information(self, "警告", "安装完成后重新运行一下本程序。")
            sys.exit()

    def saveconfig(self):
        """
        保存配置文件
        :return:
        """
        config = yaml.safe_load(open(get_file("config.yaml"), 'r', encoding='utf-8'))
        try:
            config["main"]["cron_enable"] = self.Chk_Auto.isChecked()
            config["multi"]["multi_enable"] = self.Chk_Muilt.isChecked()
            row_idx = 1
            for i in range(0, 10):
                try:
                    if self.KeyTable.item(i, 0).text() != '' or self.KeyTable.item(i, 1).text() != '':
                        config["multi"]["port" + str(row_idx)] = int(self.KeyTable.item(i, 0).text())
                        config["multi"]["key" + str(row_idx)] = self.KeyTable.item(i, 1).text()
                        row_idx += 1
                except Exception as e:
                    print(str(e))
        except:
            pass

        config["cookie"] = self.Txt_Cookie.toPlainText()
        config["sms_captcha"]["jd_wstool"] = bool(1 - self.Chk_LocalMsg.isChecked())
        config["shop"]["add_remote_shop_data"] = self.Chk_CloudID.isChecked()
        config["selenium"]["headless"] = self.Chk_Headless.isChecked()

        with open(get_file("config.yaml"), "w", encoding="utf-8") as f:
            yaml.dump(config, f)

    def Btn_Run_Clicked(self):
        """
        跑啊~~~~
        :return:
        """
        # 备份配置文件
        print(os.path.exists("./config.yaml.bak1"))
        if os.path.exists("./config.yaml.bak1") == False:
            from shutil import copy
            print("备份原始config.yaml")
            copy("config.yaml", "config.yaml.bak1")
        # 保存配置
        print("保存配置到config.yaml")
        self.saveconfig()

        print("检测python环境")
        self.GetPythonCmd()

        print("检测依赖是否正常")
        if not self.CheckModuleState():
            print("依赖不正常，进行自动安装")
            if not self.Btn_InstallPip_Clicked():
                return

        if self.Chk_Xiaobai.isChecked():
            # 检测并下载chromedriver
            if not check_driver_version(".\drivers\chromedriver.exe"):
                QMessageBox.information(self, '错误', 'chrome检测错误，请确认是否安装了chrome？不要用绿色版。')


        import threading
        threading.Thread(target=self.Run).start()

    def logout(self, idx, pinname, infoleval, info):
        if self.LogTab.tabText(idx - 1) != pinname:
            self.LogTab.setTabVisible(idx - 1, True)
            self.LogTab.setTabText(idx - 1, pinname)
        if self.OnlyShowErr.isChecked() and infoleval == 1:
                return
        self.logtext[idx - 1].append(info)

    def changeConfigFileByKey(self, ck, port):
        with open("./config.yaml", "r", encoding='UTF-8') as f:

            res_str = ''
            for line in f.readlines():
                if 'cookie:' in line:
                    line = 'cookie: "' + ck + '"\n'
                if 'smsport' in line:
                    line = line.split(':')[0] + ': ' + str(port) + '\n'
                if 'ws_conn_url' in line:
                    line = '  ws_conn_url: "ws://localhost:{}/subscribe"\n'.format(str(port))
                res_str += line

        f = open("./config.yaml", "w", encoding='UTF-8')
        f.write(res_str)
        f.close()

    def runMain(self):
        """
        根据不同平台运行退会主程序
        windows采用分窗口独立运行
        其他系统采用直接运行
        :return:
        """
        if (sys_type == 'Windows'):
            res = os.popen("python --version")
            res = res.read()
            f = open("./runmain.bat", "w", encoding='UTF-8')
            if 'python 3'.upper() in res.upper():
                f.write('start /wait cmd /C python ' + 'main.py')
            else:
                f.write('start /wait cmd /C python3 ' + 'main.py')
            f.close()
            os.system('runmain.bat')
        else:
            if (sys_type == 'Linux'):
                JDMemberCloseAccount().main()
            else:
                JDMemberCloseAccount().main()

    def runByPort(self, idx, keylist, port):
        """
        根据端口运行主代码
        :param keylist:
        :param port:
        :return:
        """
        keys = keylist.split("&")
        for key in keys:
            pin = key.split(";")[0]
            if "wskey" in key:
                print("转化wskey:" + pin + "\n")
                return_ws = getToken(key)
                if return_ws[0]:
                    key = return_ws[1]
                else:
                    print("wskey转cookie失败")
            else:
                if "pt_key" not in key:
                    return
            self.changeConfigFileByKey(key, port)
            if not self.Chk_LocalMsg.isChecked():
                os.popen(r"jd_wstool.exe -port " + str(port))
            close_task = JDMemberCloseAccount()
            close_task.logout.connect(self.logout)
            close_task.init(idx)
            close_task.main()
            # runMain()

    def runcmdlinux(self, cmd):
        """
        linux下运行指令
        :param cmd:
        :return:
        """
        import subprocess
        user_str = subprocess.getoutput(cmd)
        user_list = user_str.splitlines()  # 列表形式分隔文件内容(默认按行分隔)
        for i in user_list:
            u_info = i.split(':')
            print("username is {} uid is ".format(u_info[0], u_info[2]))

    def close_process(self, process_name):
        """
        windows端关闭制定进程
        :param process_name:
        :return:
        """
        if process_name[-4:].lower() != ".exe":
            process_name += ".exe"
        os.system("taskkill /f /im " + process_name)

    def closeAllChrome(self):
        """
        关闭所有chrome浏览器
        :return:
        """
        print("关闭chrome进程")
        try:
            if sys_type == 'Windows':
                self.close_process("chrome.exe")
                self.close_process("jd_wstool.exe")
            else:
                if sys_type == 'Linux':
                    self.runcmdlinux("mykill chrome")
                    self.runcmdlinux("mykill jd_wstool")
                else:
                    print('其他')
        except:
            print("关闭进程有错误")

    def Multi_Close(self):

        for i in range(self.LogTab.count()):
            self.LogTab.setTabVisible(i, False)
            self.LogTab.setTabText(i, "")
            self.logtext[i].setText("")

        multi_enable = get_config()["multi"]["multi_enable"]

        if not multi_enable:
            self.changeConfigFileByKey(get_config()["cookie"], 5201)
            if not self.Chk_LocalMsg.isChecked():
                os.popen(r"jd_wstool.exe -port " + str(5201))
            close_task = JDMemberCloseAccount()
            close_task.logout.connect(self.logout)
            close_task.init()
            close_task.main()
            return

        succlen = 0
        thread_list = []
        threadnum = 0
        for i in range(10):
            try:
                if self.ChkEnable[i].checkState() != QtCore.Qt.Checked:
                    continue

                if threadnum != 0:
                    time.sleep(60)  # 根据单个端口包含的swkey数量确认延时时间，保证修改config文件时不会冲突混乱

                key = get_config()["multi"]["key" + str(i + 1)]
                port = get_config()["multi"]["port" + str(i + 1)]
                if key != '' and port != '' and int(port):
                    thread_list.append(threading.Thread(target=self.runByPort, args=(i + 1, key, port)))
                    thread_list[len(thread_list) - 1].start()
                    threadnum += 1
            except:
                pass

        # 等待所有的号都退完后关闭chrome
        for i in range(len(thread_list)):
            thread_list[i].join()
        self.closeAllChrome()

    def Run(self):
        self.closeAllChrome()
        print("\n开启自动退会功能\n")

        # 启动一次立即执行
        self.Multi_Close()

        # 定时自动退会相关
        if get_config()["main"]["cron_enable"]:
            cron = get_config()["main"]["cron"]
            if len(cron.split(" ")) != 5:
                print("cron.cron 定时设置错误，必须为5位")
                return
            from apscheduler.schedulers.blocking import BlockingScheduler
            from apscheduler.triggers.cron import CronTrigger
            print("开启定时")
            scheduler = BlockingScheduler(timezone='Asia/Shanghai')
            scheduler.add_job(self.Multi_Close, CronTrigger.from_crontab(cron))
            scheduler.start()


def get_file(file_name=""):
    """
    获取文件绝对路径, 防止在某些情况下报错
    :param file_name: 文件名
    :return:
    """
    return os.path.join(os.path.split(sys.argv[0])[0], file_name)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = JDMCA_Tools()
    myshow.show()
    sys.exit(app.exec_())
