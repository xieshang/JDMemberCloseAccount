# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'JDMCA_Form.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_JDMCA(object):
    def setupUi(self, JDMCA):
        JDMCA.setObjectName("JDMCA")
        JDMCA.resize(673, 724)
        self.Btn_Run = QtWidgets.QPushButton(JDMCA)
        self.Btn_Run.setGeometry(QtCore.QRect(537, 327, 131, 51))
        self.Btn_Run.setObjectName("Btn_Run")
        self.groupBox = QtWidgets.QGroupBox(JDMCA)
        self.groupBox.setGeometry(QtCore.QRect(6, 2, 661, 121))
        self.groupBox.setObjectName("groupBox")
        self.Cookie = QtWidgets.QLabel(self.groupBox)
        self.Cookie.setGeometry(QtCore.QRect(10, 42, 54, 12))
        self.Cookie.setObjectName("Cookie")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 20, 530, 18))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Chk_Muilt = QtWidgets.QCheckBox(self.layoutWidget)
        self.Chk_Muilt.setObjectName("Chk_Muilt")
        self.horizontalLayout.addWidget(self.Chk_Muilt)
        self.Chk_Auto = QtWidgets.QCheckBox(self.layoutWidget)
        self.Chk_Auto.setObjectName("Chk_Auto")
        self.horizontalLayout.addWidget(self.Chk_Auto)
        self.Chk_LocalMsg = QtWidgets.QCheckBox(self.layoutWidget)
        self.Chk_LocalMsg.setObjectName("Chk_LocalMsg")
        self.horizontalLayout.addWidget(self.Chk_LocalMsg)
        self.Chk_CloudID = QtWidgets.QCheckBox(self.layoutWidget)
        self.Chk_CloudID.setObjectName("Chk_CloudID")
        self.horizontalLayout.addWidget(self.Chk_CloudID)
        self.Chk_Headless = QtWidgets.QCheckBox(self.layoutWidget)
        self.Chk_Headless.setObjectName("Chk_Headless")
        self.horizontalLayout.addWidget(self.Chk_Headless)
        self.Chk_Xiaobai = QtWidgets.QCheckBox(self.layoutWidget)
        self.Chk_Xiaobai.setChecked(True)
        self.Chk_Xiaobai.setObjectName("Chk_Xiaobai")
        self.horizontalLayout.addWidget(self.Chk_Xiaobai)
        self.Txt_Cookie = QtWidgets.QLineEdit(self.groupBox)
        self.Txt_Cookie.setGeometry(QtCore.QRect(10, 60, 641, 51))
        self.Txt_Cookie.setObjectName("Txt_Cookie")
        self.KeyTable = QtWidgets.QTableWidget(JDMCA)
        self.KeyTable.setGeometry(QtCore.QRect(6, 127, 661, 191))
        self.KeyTable.setObjectName("KeyTable")
        self.KeyTable.setColumnCount(3)
        self.KeyTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.KeyTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.KeyTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.KeyTable.setHorizontalHeaderItem(2, item)
        self.layoutWidget1 = QtWidgets.QWidget(JDMCA)
        self.layoutWidget1.setGeometry(QtCore.QRect(11, 321, 324, 25))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Btn_InstallPip = QtWidgets.QPushButton(self.layoutWidget1)
        self.Btn_InstallPip.setObjectName("Btn_InstallPip")
        self.horizontalLayout_3.addWidget(self.Btn_InstallPip)
        self.Combox_mirror = QtWidgets.QComboBox(self.layoutWidget1)
        self.Combox_mirror.setObjectName("Combox_mirror")
        self.Combox_mirror.addItem("")
        self.Combox_mirror.addItem("")
        self.Combox_mirror.addItem("")
        self.Combox_mirror.addItem("")
        self.horizontalLayout_3.addWidget(self.Combox_mirror)
        self.Btn_unInstallPip = QtWidgets.QPushButton(self.layoutWidget1)
        self.Btn_unInstallPip.setObjectName("Btn_unInstallPip")
        self.horizontalLayout_3.addWidget(self.Btn_unInstallPip)
        self.Btn_downchromedriver = QtWidgets.QPushButton(self.layoutWidget1)
        self.Btn_downchromedriver.setObjectName("Btn_downchromedriver")
        self.horizontalLayout_3.addWidget(self.Btn_downchromedriver)
        self.layoutWidget2 = QtWidgets.QWidget(JDMCA)
        self.layoutWidget2.setGeometry(QtCore.QRect(11, 350, 363, 25))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.layoutWidget2)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.Txt_ModuleName = QtWidgets.QLineEdit(self.layoutWidget2)
        self.Txt_ModuleName.setObjectName("Txt_ModuleName")
        self.horizontalLayout_2.addWidget(self.Txt_ModuleName)
        self.Btn_InstallPip_One = QtWidgets.QPushButton(self.layoutWidget2)
        self.Btn_InstallPip_One.setObjectName("Btn_InstallPip_One")
        self.horizontalLayout_2.addWidget(self.Btn_InstallPip_One)
        self.Btn_unInstallPip_One = QtWidgets.QPushButton(self.layoutWidget2)
        self.Btn_unInstallPip_One.setObjectName("Btn_unInstallPip_One")
        self.horizontalLayout_2.addWidget(self.Btn_unInstallPip_One)
        self.LogTab = QtWidgets.QTabWidget(JDMCA)
        self.LogTab.setGeometry(QtCore.QRect(1, 380, 671, 341))
        self.LogTab.setObjectName("LogTab")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.LogText_1 = QtWidgets.QTextEdit(self.tab_1)
        self.LogText_1.setGeometry(QtCore.QRect(3, 4, 661, 311))
        self.LogText_1.setObjectName("LogText_1")
        self.LogTab.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.LogText_2 = QtWidgets.QTextEdit(self.tab_2)
        self.LogText_2.setGeometry(QtCore.QRect(3, 3, 661, 311))
        self.LogText_2.setObjectName("LogText_2")
        self.LogTab.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.LogText_3 = QtWidgets.QTextEdit(self.tab_3)
        self.LogText_3.setGeometry(QtCore.QRect(2, 3, 661, 311))
        self.LogText_3.setObjectName("LogText_3")
        self.LogTab.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.LogText_4 = QtWidgets.QTextEdit(self.tab_4)
        self.LogText_4.setGeometry(QtCore.QRect(3, 3, 661, 311))
        self.LogText_4.setObjectName("LogText_4")
        self.LogTab.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.LogText_5 = QtWidgets.QTextEdit(self.tab_5)
        self.LogText_5.setGeometry(QtCore.QRect(2, 3, 661, 311))
        self.LogText_5.setObjectName("LogText_5")
        self.LogTab.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.LogText_6 = QtWidgets.QTextEdit(self.tab_6)
        self.LogText_6.setGeometry(QtCore.QRect(2, 3, 661, 311))
        self.LogText_6.setObjectName("LogText_6")
        self.LogTab.addTab(self.tab_6, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.LogText_7 = QtWidgets.QTextEdit(self.tab_7)
        self.LogText_7.setGeometry(QtCore.QRect(3, 3, 661, 311))
        self.LogText_7.setObjectName("LogText_7")
        self.LogTab.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.LogText_8 = QtWidgets.QTextEdit(self.tab_8)
        self.LogText_8.setGeometry(QtCore.QRect(2, 3, 661, 311))
        self.LogText_8.setObjectName("LogText_8")
        self.LogTab.addTab(self.tab_8, "")
        self.OnlyShowErr = QtWidgets.QCheckBox(JDMCA)
        self.OnlyShowErr.setGeometry(QtCore.QRect(540, 380, 131, 20))
        self.OnlyShowErr.setObjectName("OnlyShowErr")

        self.retranslateUi(JDMCA)
        self.LogTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(JDMCA)
        JDMCA.setTabOrder(self.Chk_Muilt, self.Chk_LocalMsg)
        JDMCA.setTabOrder(self.Chk_LocalMsg, self.Chk_Auto)
        JDMCA.setTabOrder(self.Chk_Auto, self.Chk_CloudID)
        JDMCA.setTabOrder(self.Chk_CloudID, self.Chk_Headless)
        JDMCA.setTabOrder(self.Chk_Headless, self.KeyTable)
        JDMCA.setTabOrder(self.KeyTable, self.Btn_Run)

    def retranslateUi(self, JDMCA):
        _translate = QtCore.QCoreApplication.translate
        JDMCA.setWindowTitle(_translate("JDMCA", "退会无脑工具"))
        self.Btn_Run.setText(_translate("JDMCA", "跑"))
        self.groupBox.setTitle(_translate("JDMCA", "设置"))
        self.Cookie.setText(_translate("JDMCA", "Cookie："))
        self.Chk_Muilt.setText(_translate("JDMCA", "多账号同退"))
        self.Chk_Auto.setWhatsThis(_translate("JDMCA", "<html><head/><body><p>开启自动退会，定时时间自己改config.yaml</p></body></html>"))
        self.Chk_Auto.setText(_translate("JDMCA", "定时自动退会"))
        self.Chk_LocalMsg.setWhatsThis(_translate("JDMCA", "<html><head/><body><p>使用内建的短信接收器，不要再运行jd_wstool，否则验证码接收失败。</p></body></html>"))
        self.Chk_LocalMsg.setText(_translate("JDMCA", "短信内部监听"))
        self.Chk_CloudID.setWhatsThis(_translate("JDMCA", "<html><head/><body><p>退隐藏店铺会员卡，浏览器会出现很多“网络请求失败”，请忽略</p></body></html>"))
        self.Chk_CloudID.setText(_translate("JDMCA", "云店铺列表"))
        self.Chk_Headless.setWhatsThis(_translate("JDMCA", "<html><head/><body><p>不想看到浏览器的影子，就打钩。</p></body></html>"))
        self.Chk_Headless.setText(_translate("JDMCA", "无头模式"))
        self.Chk_Xiaobai.setWhatsThis(_translate("JDMCA", "<html><head/><body><p>不想看到浏览器的影子，就打钩。</p></body></html>"))
        self.Chk_Xiaobai.setText(_translate("JDMCA", "我是小白"))
        item = self.KeyTable.horizontalHeaderItem(0)
        item.setText(_translate("JDMCA", "运行"))
        item = self.KeyTable.horizontalHeaderItem(1)
        item.setText(_translate("JDMCA", "端口"))
        item = self.KeyTable.horizontalHeaderItem(2)
        item.setText(_translate("JDMCA", "Key"))
        self.Btn_InstallPip.setText(_translate("JDMCA", "安装依赖"))
        self.Combox_mirror.setItemText(0, _translate("JDMCA", "豆瓣"))
        self.Combox_mirror.setItemText(1, _translate("JDMCA", "清华"))
        self.Combox_mirror.setItemText(2, _translate("JDMCA", "腾讯"))
        self.Combox_mirror.setItemText(3, _translate("JDMCA", "阿里"))
        self.Btn_unInstallPip.setText(_translate("JDMCA", "卸载依赖"))
        self.Btn_downchromedriver.setText(_translate("JDMCA", "下载chromedriver"))
        self.label.setText(_translate("JDMCA", "单独依赖："))
        self.Btn_InstallPip_One.setText(_translate("JDMCA", "安装"))
        self.Btn_unInstallPip_One.setText(_translate("JDMCA", "卸载"))
        self.LogTab.setTabText(self.LogTab.indexOf(self.tab_1), _translate("JDMCA", "Tab 1"))
        self.LogTab.setTabText(self.LogTab.indexOf(self.tab_2), _translate("JDMCA", "2"))
        self.LogTab.setTabText(self.LogTab.indexOf(self.tab_3), _translate("JDMCA", "页"))
        self.LogTab.setTabText(self.LogTab.indexOf(self.tab_4), _translate("JDMCA", "页"))
        self.LogTab.setTabText(self.LogTab.indexOf(self.tab_5), _translate("JDMCA", "页"))
        self.LogTab.setTabText(self.LogTab.indexOf(self.tab_6), _translate("JDMCA", "页"))
        self.LogTab.setTabText(self.LogTab.indexOf(self.tab_7), _translate("JDMCA", "页"))
        self.LogTab.setTabText(self.LogTab.indexOf(self.tab_8), _translate("JDMCA", "页"))
        self.OnlyShowErr.setText(_translate("JDMCA", "只显示重要的信息"))
