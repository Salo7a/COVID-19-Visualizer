# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(922, 711)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Deaths = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.Deaths.setFont(font)
        self.Deaths.setMouseTracking(False)
        self.Deaths.setScaledContents(True)
        self.Deaths.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.Deaths.setObjectName("Deaths")
        self.horizontalLayout_2.addWidget(self.Deaths)
        self.DeathsNew = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DeathsNew.setFont(font)
        self.DeathsNew.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.DeathsNew.setObjectName("DeathsNew")
        self.horizontalLayout_2.addWidget(self.DeathsNew)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.DeathText = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DeathText.sizePolicy().hasHeightForWidth())
        self.DeathText.setSizePolicy(sizePolicy)
        self.DeathText.setAlignment(QtCore.Qt.AlignCenter)
        self.DeathText.setObjectName("DeathText")
        self.verticalLayout_2.addWidget(self.DeathText)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.Cases = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.Cases.setFont(font)
        self.Cases.setScaledContents(True)
        self.Cases.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Cases.setObjectName("Cases")
        self.horizontalLayout_4.addWidget(self.Cases)
        self.CasesNew = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.CasesNew.setFont(font)
        self.CasesNew.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.CasesNew.setObjectName("CasesNew")
        self.horizontalLayout_4.addWidget(self.CasesNew)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.CasesText = QtWidgets.QLabel(self.groupBox_3)
        self.CasesText.setAlignment(QtCore.Qt.AlignCenter)
        self.CasesText.setObjectName("CasesText")
        self.verticalLayout_3.addWidget(self.CasesText)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.Recovered = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.Recovered.setFont(font)
        self.Recovered.setScaledContents(True)
        self.Recovered.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.Recovered.setObjectName("Recovered")
        self.horizontalLayout_5.addWidget(self.Recovered)
        self.RecoveredNew = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.RecoveredNew.setFont(font)
        self.RecoveredNew.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.RecoveredNew.setObjectName("RecoveredNew")
        self.horizontalLayout_5.addWidget(self.RecoveredNew)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.RecoveredYext = QtWidgets.QLabel(self.groupBox_3)
        self.RecoveredYext.setAlignment(QtCore.Qt.AlignCenter)
        self.RecoveredYext.setObjectName("RecoveredYext")
        self.verticalLayout_4.addWidget(self.RecoveredYext)
        self.gridLayout_3.addLayout(self.verticalLayout_4, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Bubble = QtWidgets.QRadioButton(self.groupBox_2)
        self.Bubble.setObjectName("Bubble")
        self.horizontalLayout.addWidget(self.Bubble)
        self.Map = QtWidgets.QRadioButton(self.groupBox_2)
        self.Map.setObjectName("Map")
        self.horizontalLayout.addWidget(self.Map)
        self.BarCases = QtWidgets.QRadioButton(self.groupBox_2)
        self.BarCases.setObjectName("BarCases")
        self.horizontalLayout.addWidget(self.BarCases)
        self.BarDeaths = QtWidgets.QRadioButton(self.groupBox_2)
        self.BarDeaths.setObjectName("BarDeaths")
        self.horizontalLayout.addWidget(self.BarDeaths)
        self.EBubble = QtWidgets.QRadioButton(self.groupBox_2)
        self.EBubble.setObjectName("EBubble")
        self.horizontalLayout.addWidget(self.EBubble)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_3.addWidget(self.line)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox.setFlat(True)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.Update = QtWidgets.QPushButton(self.groupBox)
        self.Update.setObjectName("Update")
        self.gridLayout.addWidget(self.Update, 0, 0, 1, 1)
        self.Export = QtWidgets.QPushButton(self.groupBox)
        self.Export.setObjectName("Export")
        self.gridLayout.addWidget(self.Export, 1, 0, 1, 1)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.browser = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browser.sizePolicy().hasHeightForWidth())
        self.browser.setSizePolicy(sizePolicy)
        self.browser.setMinimumSize(QtCore.QSize(300, 400))
        self.browser.setObjectName("browser")
        self.gridLayout_2.addWidget(self.browser, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 922, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Live Stats (Updated Every 10 Minutes):"))
        self.Deaths.setToolTip(_translate("MainWindow", "Total Deaths"))
        self.Deaths.setText(_translate("MainWindow", "TextLabel"))
        self.DeathsNew.setText(_translate("MainWindow", "TextLabel"))
        self.DeathText.setText(_translate("MainWindow", "Deaths"))
        self.Cases.setToolTip(_translate("MainWindow", "Total Cases"))
        self.Cases.setText(_translate("MainWindow", "TextLabel"))
        self.CasesNew.setText(_translate("MainWindow", "TextLabel"))
        self.CasesText.setText(_translate("MainWindow", "Confirmed"))
        self.Recovered.setToolTip(_translate("MainWindow", "Total Recovered"))
        self.Recovered.setWhatsThis(_translate("MainWindow", "Total Recovered Cases"))
        self.Recovered.setText(_translate("MainWindow", "TextLabel"))
        self.RecoveredNew.setText(_translate("MainWindow", "TextLabel"))
        self.RecoveredYext.setText(_translate("MainWindow", "Recovered"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Plot Select:"))
        self.Bubble.setText(_translate("MainWindow", "Cases Bubble Plot"))
        self.Map.setText(_translate("MainWindow", "World Map"))
        self.BarCases.setText(_translate("MainWindow", "Bar By Cases"))
        self.BarDeaths.setText(_translate("MainWindow", "Bar By Deaths"))
        self.EBubble.setText(_translate("MainWindow", "Death Rate"))
        self.groupBox.setTitle(_translate("MainWindow", "Tools"))
        self.Update.setText(_translate("MainWindow", "Update Database"))
        self.Export.setText(_translate("MainWindow", "Export To Video File"))
from PyQt5 import QtWebEngineWidgets
