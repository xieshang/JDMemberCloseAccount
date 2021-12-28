import os
import sys

import yaml
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem

from JDMCA_Form import Ui_JDMCA
from utils.config import get_config


class JDMCA_Tools(QtWidgets.QWidget, Ui_JDMCA):
    def Log_info(self, log):
        self.logbox.setPlainText(self.logbox.toPlainText() + log + "\n")


    def __init__(self):
        super(JDMCA_Tools, self).__init__()
        self.setupUi(self)
        self.resize(self.width(), self.height())
        self.setMaximumSize(self.width(), self.height())
        self.setMinimumSize(self.width(), self.height())
        self.form_max_height = self.height()
        self.KeyTable.setColumnWidth(0, 80)
        self.KeyTable.setColumnWidth(1, 550)
        row_cnt = self.KeyTable.rowCount()
        for i in range(12):
            self.KeyTable.insertRow(row_cnt)
        self.Chk_Muilt.clicked.connect(self.Chk_Muilt_Clicked)
        self.Btn_Run.clicked.connect(self.Btn_Run_Clicked)
        self.init()



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
        self.Chk_Auto.setChecked(config["main"]["auto"])
        self.Txt_Cookie.setPlainText(config["cookie"])
        self.Chk_Muilt.setChecked(config["multi"]["multi"])
        self.Chk_LocalMsg.setChecked(1 - config["sms_captcha"]["jd_wstool"])
        self.Chk_CloudID.setChecked(config["shop"]["add_remote_shop_data"])
        self.Chk_Headless.setChecked(config["selenium"]["headless"])

        row_idx = 0
        for i in range(1, 10):
            try:
                self.KeyTable.setItem(row_idx, 0, QTableWidgetItem(str(config["multi"]["port"+str(i)])))
                self.KeyTable.setItem(row_idx, 1, QTableWidgetItem(config["multi"]["key"+str(i)]))
                row_idx += 1
            except Exception as e:
                print(str(e))
        self.Chk_Muilt_Clicked()
        pass


    def saveconfig(self):
        config = yaml.safe_load(open(get_file("config.yaml"), 'r', encoding='utf-8'))
        config["main"]["auto"] = self.Chk_Auto.isChecked()
        config["cookie"] = self.Txt_Cookie.toPlainText()
        config["multi"]["multi"] = self.Chk_Muilt.isChecked()
        config["sms_captcha"]["jd_wstool"] = bool(1 - self.Chk_LocalMsg.isChecked())
        config["shop"]["add_remote_shop_data"] = self.Chk_CloudID.isChecked()
        config["selenium"]["headless"] = self.Chk_Headless.isChecked()

        row_idx = 1
        for i in range(0, 10):
            try:
                if self.KeyTable.item(i, 0).text() != '' or self.KeyTable.item(i, 1).text() != '':
                    config["multi"]["port" + str(row_idx)] = int(self.KeyTable.item(i, 0).text())
                    config["multi"]["key"+str(row_idx)] = self.KeyTable.item(i, 1).text()
                    row_idx += 1
            except Exception as e:
                print(str(e))

        with open(get_file("config.yaml"), "w", encoding="utf-8") as f:
            yaml.dump(config, f)


    def Btn_Run_Clicked(self):
        # 保存配置
        # 备份配置文件
        print(os.path.exists("./config.yaml.bak1"))
        if os.path.exists("./config.yaml.bak1") == False:
            from shutil import copy
            copy("./config.yaml", "./config.yaml.bak1")
        self.saveconfig()
        res = os.popen("python --version")
        res = res.read()
        if 'python'.upper() in res.upper():
            cmd = ('start cmd /C python ' + 'Multi_Close.py')
        else:
            cmd =('start cmd /C python3 ' + 'Multi_Close.py')
        os.popen(cmd)


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
