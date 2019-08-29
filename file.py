# -*- coding: utf-8 -*-
# indeed-scraper.py

from PyQt5 import QtCore, QtGui, QtWidgets
import requests, pyfiglet, sys
from bs4 import BeautifulSoup
from colorama import Fore
import colorama, time, random
import pymysql.cursors
colorama.init()
import requests, re
from bs4 import BeautifulSoup
import pyfiglet
import pandas as pd
import colorama, shutil
from colorama import Fore
colorama.init()
cols, rows = shutil.get_terminal_size()


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(527, 330)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 290, 301, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setItalic(True)
        self.pushButton.setFont(font)
        self.pushButton.clicked.connect(self.scraper)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(90, 10, 241, 21))
        font = QtGui.QFont()
        font.setItalic(True)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 10, 61, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 40, 241, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setIndent(1)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(380, -10, 231, 61))
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setItalic(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(380, 20, 211, 41))
        font = QtGui.QFont()
        font.setFamily("URW Bookman L")
        font.setItalic(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 260, 301, 23))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(11)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(40, 70, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setIndent(1)
        self.label_5.setObjectName("label_5")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(90, 70, 241, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(400, 310, 59, 15))
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def scraper(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_3.setText(_translate("Dialog", "Status: RUNNING"))
        session = requests.Session()
        session.headers.update(
            {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"})
        indeed_cookies = session.get("https://www.indeed.com")
        page = 0
        query = self.lineEdit.text()
        location = self.lineEdit_2.text()
        stop_on_page = self.lineEdit_3.text()
        job_titles = []
        employers = []
        self.progressBar.setProperty("value", 0)
        counter = 0
        for i in range(int(stop_on_page)):
            programmer = session.get(f"https://www.indeed.com/jobs?q={query}&l={location}&start={page}")
            page += 10
            soup = BeautifulSoup(programmer.text, "html.parser")
            jobs = soup.findAll('a', attrs={"data-tn-element": "jobTitle"})
            companies = soup.findAll('a', attrs={"data-tn-element": "companyName"})
            counter += 5.9
            self.progressBar.setProperty("value", counter)
            for job in jobs:
                job_titles.append(job.get('title'))
                self.label_4.setText(_translate("Dialog", "Scraped: %d" % len(job_titles)))
            for company in companies:
                employers.append(company.text.strip())
            self.label_2.setText(_translate("Dialog", "Location"))
        while len(employers) != len(job_titles):
            employers.append("NaN")
            self.progressBar.setProperty("value", 0.10)
        print(len(job_titles))
        data = {'Job Title': job_titles, 'Employer': employers}
        dataframe = pd.DataFrame(data=data)
        dataframe.to_excel('indeed.xlsx', sheet_name='Indeed')
        self.progressBar.setProperty("value", 100)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "The Birger"))
        self.pushButton.setText(_translate("Dialog", "Scrape"))
        self.label.setText(_translate("Dialog", "Query"))
        self.label_2.setText(_translate("Dialog", "Location"))
        self.label_3.setText(_translate("Dialog", "Status:"))
        self.label_4.setText(_translate("Dialog", "Scraped: "))
        self.label_5.setText(_translate("Dialog", "Stop"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
