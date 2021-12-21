import sys

from PyQt5 import QtWidgets

from JDMCA_Form import Ui_JDMCA
from utils.config import get_config


class JDMCA_Tools(QtWidgets.QWidget, Ui_JDMCA):
    def Log_info(self, log):
        self.logbox.setPlainText(self.logbox.toPlainText() + log + "\n")


    def __init__(self):
        super(JDMCA_Tools, self).__init__()
        self.setupUi(self)
        self.init()
        self.resize(self.width(), self.height())
        self.setMaximumSize(self.width(), self.height())
        self.setMinimumSize(self.width(), self.height())
        self.form_max_height = self.height()

    def init(self):
        self.Text_CK.setPlainText(get_config()["cookie"])
        self.Btn_Run.clicked.connect(self.Btn_Run_Clicked)

    def ChangeConfig(self, dir = {}):
        with open("./config.yaml", "r", encoding='UTF-8') as f:

            res_str = ''
            for line in f.readlines():
                for key,val in dir:
                    if key in line:
                        line = line.split('"')[0] + '"' + str(val) + '"' + line.split('"')[2]
                    res_str += line
        f = open("./config.yaml", "w", encoding='UTF-8')
        f.write(res_str)
        f.close()

    def Btn_Run_Clicked(self):
        # 修改CK
        if self.Text_CK.toPlainText().find("pt_key") is None or self.Text_CK.toPlainText().find("pt_pin") is None:
            self.Log_info("Cookie有问题，请检查")
            return
        self.ChangeConfig({"cookie": self.Text_CK.toPlainText()})







if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = JDMCA_Tools()
    myshow.show()
    sys.exit(app.exec_())
