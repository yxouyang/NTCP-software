# -*- coding: gb2312 -*-
# 开发团队 : 益相工作室
# 开发人员 : 欧阳会丹
# 开发时间 : 2023/12/2 12:33
# 文件名称 : The algorithm models for NTCP prediction(V2023).py
import sys
import math
from PyQt5.QtWidgets import *
from functools import partial
from scipy import integrate
import xlrd
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon, QPixmap
import time

class WinForm(QMainWindow):
    s1 = 1
    s2 = 2
    s3 = 3
    s4 = 4
    s5 = 5

    def NTCPfProbit(self,x):
        return math.e ** (-0.5 * x ** 2)

    def NTCPProbit(self,s, u, u50):
        return (1 / ((2 * math.pi) ** 0.5)) * integrate.quad(self.NTCPfProbit, float('-inf'), s * (u - u50))[0]

    def NTCPLogit(self,k, u, u50):
        return 1.0 / (1.0 + (u50 / u) ** k)

    def NTCPSRU(self,derta, u, u50):
        return 1.0 - math.e ** (-1.0 * math.e ** (derta * (u - u50)))

    def NTCPPoisson(self,a, u, u50):
        return 1.0 - math.e ** (-1.0 * math.log(2) * (u / u50) ** a)

    def NTCPlogistic(self,b1, u, b2):
        return 1.0 / (1.0 + math.e ** (-b1 - b2 * u))

    def __init__(self,parent=None):
        super(WinForm, self).__init__(parent)
        self.setWindowTitle('5 NTCP models')
        self.setGeometry(300,300,600,400)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        font1 = QFont()
        font1.setPointSize(15)
        label = QLabel('Software developers：Huidan OuYang;Yuze Liu;Zhenyu Xu;Lei Zeng\nOrganizations：Jiangxi Agricultural University;\nThe second affiliated hospital of Nanchang university \nYear：2024')
        label.setStyleSheet("QLabel { color : #ff0000; }")
        label.setFont(font1)
        label2 = QLabel('The algorithm models for NTCP prediction：')
        label2.setStyleSheet("QLabel { color : #ff0000; }")
        label2.setFont(font)
        buttonProbit = QPushButton('Lyman Algorithm Model')
        buttonLogit = QPushButton('Logit Algorithm Model')
        buttonSRU = QPushButton('SRU Algorithm Model')
        buttonPoisson = QPushButton('Poisson Algorithm Model')
        buttonlogisitic = QPushButton('Logisitic Algorithm Model')
        buttonProbit.setFont(font)
        buttonLogit.setFont(font)
        buttonSRU.setFont(font)
        buttonPoisson.setFont(font)
        buttonlogisitic.setFont(font)
        buttonProbit.clicked.connect(partial(self.Probit, self.s1))
        buttonLogit.clicked.connect(partial(self.Logit, self.s2))
        buttonSRU.clicked.connect(partial(self.SRU, self.s3))
        buttonPoisson.clicked.connect(partial(self.Poisson, self.s4))
        buttonlogisitic.clicked.connect(partial(self.logisitic, self.s5))
        main=QWidget()
        # main.setStyleSheet('border-image:url(./i3.png);')
        self.setWindowIcon(QIcon('./i2.ico'))
        layout=QVBoxLayout(main)
        layout.addWidget(label2)
        layout.addWidget(buttonProbit)
        layout.addWidget(buttonLogit)
        layout.addWidget(buttonSRU)
        layout.addWidget(buttonPoisson)
        layout.addWidget(buttonlogisitic)
        layout.addWidget(label)
        self.setCentralWidget(main)

    def Probit(self,n):
        eud = 0
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, 'Select an Excel file', '', 'Excel文件(*.xlsx *.xls)', options=options)
        if fileName:
            print('fileName', fileName)
            workbook = xlrd.open_workbook(fileName)
            sheet = workbook.sheet_by_index(0)
            content1 = sheet.col_values(0)
            content2 = sheet.col_values(1)
        for i in range(len(content1)):
            eud += float(content1[i]) ** 15 * float(content2[i])
        eud = eud ** (1/15)
        print(eud)
        print('The Lyman model predicts NTCP results：{0}'.format(self.NTCPProbit(0.15,eud,76)))
        QMessageBox.information(self, 'Predicting temporal lobe injury', 'The Lyman model predicts NTCP results：{0}'.format(self.NTCPProbit(0.15,eud,76)))

    def Logit(self,n):
        eud = 0
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, 'Select an Excel file', '', 'Excel文件(*.xlsx *.xls)', options=options)
        if fileName:
            print('fileName', fileName)
            workbook = xlrd.open_workbook(fileName)
            sheet = workbook.sheet_by_index(0)
            content1 = sheet.col_values(0)
            content2 = sheet.col_values(1)
        for i in range(len(content1)):
            eud += float(content1[i]) ** 16 * float(content2[i])
        eud = eud ** (1 / 16)
        print(eud)
        print('The Logit model predicts NTCP results：{0}'.format(self.NTCPLogit(20,eud,80)))
        QMessageBox.information(self, 'Predicting temporal lobe injury', 'The Logit model predicts NTCP results：{0}'.format(self.NTCPLogit(20,eud,80)))
    def SRU(self,n):
        eud = 0
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, 'Select an Excel file', '', 'Excel文件(*.xlsx *.xls)', options=options)
        if fileName:
            print('fileName', fileName)
            workbook = xlrd.open_workbook(fileName)
            sheet = workbook.sheet_by_index(0)
            content1 = sheet.col_values(0)
            content2 = sheet.col_values(1)
        for i in range(len(content1)):
            eud += content2[i] * math.e ** (0.179 * content1[i])
        eud= math.log(eud) * (1 / 0.179)
        print(eud)
        print('The SRU model predicts NTCP results：{0}'.format(self.NTCPSRU(0.179, eud, 80)))
        QMessageBox.information(self, 'Predicting temporal lobe injury', 'The SRU model predicts NTCP results：{0}'.format(self.NTCPSRU(0.179, eud, 80)))
    def Poisson(self,n):
        eud = 0
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, 'Select an Excel file', '', 'Excel文件(*.xlsx *.xls)', options=options)
        if fileName:
            print('fileName', fileName)
            workbook = xlrd.open_workbook(fileName)
            sheet = workbook.sheet_by_index(0)
            content1 = sheet.col_values(0)
            content2 = sheet.col_values(1)
        for i in range(len(content1)):
            eud += float(content1[i]) ** 16 * float(content2[i])
        eud = eud ** (1 / 16)
        print(eud)
        print('The Poisson model predicts NTCP results：{0}'.format(self.NTCPPoisson(16, eud, 80)))
        QMessageBox.information(self, 'Predicting temporal lobe injury', 'The Poisson model predicts NTCP results：{0}'.format(self.NTCPPoisson(16, eud, 80)))
    def logisitic(self,n):
        eud = 0
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, 'Select an Excel file', '', 'Excel文件(*.xlsx *.xls)', options=options)
        if fileName:
            print('fileName', fileName)
            workbook = xlrd.open_workbook(fileName)
            sheet = workbook.sheet_by_index(0)
            content1 = sheet.col_values(0)
            content2 = sheet.col_values(1)
        for i in range(len(content1)):
            eud += float(content1[i]) ** 20 * float(content2[i])
        eud = eud ** (1 / 20)
        print(eud)
        print('The logisitic model predicts NTCP results：{0}'.format(self.NTCPlogistic(-15.7, eud, 0.2)))
        QMessageBox.information(self, 'Predicting temporal lobe injury', 'The logisitic model predicts NTCP results：{0}'.format(self.NTCPlogistic(-15.7, eud, 0.2)))

if __name__ == '__main__':
    current = time.localtime()
    print('时间：', current.tm_year)
    if current.tm_year != 2024:
        sys.exit()
    app = QApplication(sys.argv)
    form = WinForm()
    form.show()
    exit_code = app.exec()
    sys.exit(exit_code)
