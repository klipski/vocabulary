# -*- coding: utf-8 -*-
# /usr/bin/env python3

from __future__ import unicode_literals, print_function

import random
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
import unicodedata
from StringComparison import *

random.seed()

def remove_spaces(s):
    return s.replace(" ", "")


def remove_parenthess_data(s):
    result = s
    first_p = result.find("(")
    second_p = result.find(")")
    a = 0
    while (first_p >= 0 and second_p > first_p) and a < 10:
        result = result[:first_p] + result[second_p + 1:]
        first_p = result.find("(")
        second_p = result.find(")")
        a += 1
    return result


class MyApp(QDialog):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.setMinimumSize(400, 180)
        self.setWindowTitle("Check your english knowledge")
        self.layout = QGridLayout(self)

        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.check)

        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.close)

        self.skipButton = QPushButton("Skip")
        self.skipButton.clicked.connect(self.skip)

        self.label = QLabel("label")

        self.lineEdit = QLineEdit()

        self.goodAnswersCount = 0
        self.goodLabel = QLabel("Good: 0")

        self.badAnswersCount = 0
        self.badLabel = QLabel("Bad: 0")

        self.data = {}

        self.chapter1Radio = QRadioButton("Chapter 1.")
        self.chapter1Radio.setChecked(True)
        self.chapter1Radio.clicked.connect(self.loadData)
        self.chapter2Radio = QRadioButton("Chapter 2.")
        self.chapter2Radio.clicked.connect(self.loadData)
        self.allRadio = QRadioButton("All")
        self.allRadio.clicked.connect(self.loadData)
        self.latinRadio = QRadioButton("Latin expressions")
        self.latinRadio.clicked.connect(self.loadData)

        self.layout.addWidget(self.chapter1Radio, 0, 0, 1, 1)
        self.layout.addWidget(self.chapter2Radio, 0, 1, 1, 1)
        self.layout.addWidget(self.latinRadio, 0, 2, 1, 1)
        self.layout.addWidget(self.allRadio, 0, 3, 1, 1)

        self.layout.addWidget(self.label, 1, 0, 1, 4)
        self.layout.addWidget(self.lineEdit, 2, 0, 1, 4)
        self.layout.addWidget(self.okButton, 3, 0, 1, 2)
        self.layout.addWidget(self.skipButton, 3, 2, 1, 2)
        self.layout.addWidget(self.goodLabel, 5, 0, 1, 2)
        self.layout.addWidget(self.badLabel, 5, 2, 1, 2)
        # self.layout.addWidget(self.closeButton, 3, 1, 1, 1)
        self.actualword = ""
        self.polishword = ""
        self.loadData()

    def loadData(self):
        if self.chapter1Radio.isChecked():
            self.data = {}
            with open("slowka", "r") as file:
                lines = file.readlines()
                for line in lines:
                    x = line.replace("\n", "").split(";")
                    self.data[x[0]] = x[1].split("/")
        elif self.chapter2Radio.isChecked():
            self.data = {}
            with open("slowka2", "r") as file:
                lines = file.readlines()
                for line in lines:
                    x = line.replace("\n", "").split(";")
                    self.data[x[0]] = x[1].split("/")
        elif self.latinRadio.isChecked():
            self.data = {}
            with open("skroty", "r") as file:
                lines = file.readlines()
                for line in lines:
                    x = line.replace("\n", "").split(";")
                    self.data[x[0]] = x[1].split("/")
        else:
             self.data = {}
             with open("slowka", "r") as file:
                lines = file.readlines()
                for line in lines:
                    x = line.replace("\n", "").split(";")
                    self.data[x[0]] = x[1].split("/")
             with open("slowka2", "r") as file:
                lines = file.readlines()
                for line in lines:
                    x = line.replace("\n", "").split(";")
                    self.data[x[0]] = x[1].split("/")
             with open("skroty", "r") as file:
                lines = file.readlines()
                for line in lines:
                    x = line.replace("\n", "").split(";")
                    self.data[x[0]] = x[1].split("/")

        self.randWord()

    def check(self):
        answer = self.lineEdit.text()
        if self.filter(answer):
            self.goodAnswer()
            self.showProperAnswer()
            self.randWord()
        else:
            self.badAnswer()
            QMessageBox.warning(self, "Seriously?", "Wrong answer!")
        self.lineEdit.setText("")

    def skip(self):
        self.badAnswer()
        self.showProperAnswer()
        self.lineEdit.setText("")
        self.randWord()

    def showProperAnswer(self):
        if self.actualword:
            properAnswer = "/".join(self.data[self.actualword])
            QMessageBox.information(self, "Answer", "%s: %s" % (self.actualword, properAnswer))
        else:
            properAnswer = self.data[self.polishword.split("/")]
            QMessageBox.information(self, "Answer", "%s: %s" % (self.polishword, properAnswer))

    def randWord(self):
        try:
            self.actualword = random.choice(self.data.keys())
        except:
            self.actualword = random.choice(list(self.data.keys()))
        r = random.randint(0, 10)
        if r % 2:
            self.polishword = "/".join(self.data[self.actualword])
            self.label.setText(self.polishword)
        else:
            self.polishword = ""
            self.label.setText(self.actualword)

    def goodAnswer(self):
        self.goodAnswersCount += 1
        self.goodLabel.setText("Good: %d" % self.goodAnswersCount)

    def badAnswer(self):
        self.badAnswersCount += 1
        self.badLabel.setText("Bad: %d" % self.badAnswersCount)

    def filter(self, s):
        answer = remove_parenthess_data(s)
        if self.polishword:
            similar = similarity(remove_parenthess_data(self.actualword), answer)
            if similar > 75.:
                return True
        else:
            for text in self.data[self.actualword]:
                similar = similarity(remove_parenthess_data(text), answer)
                if similar > 70.:
                    return True
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
sys.exit(app.exec_())
