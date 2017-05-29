# -*- coding: utf-8 -*-
# /usr/bin/env python3

from __future__ import unicode_literals, print_function

import random
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
import unicodedata
from os import listdir
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
		self.radioButtons = {}
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

		self.layout.addWidget(self.label, 3, 0, 1, 4)
		self.layout.addWidget(self.lineEdit, 4, 0, 1, 4)
		self.layout.addWidget(self.okButton, 5, 0, 1, 2)
		self.layout.addWidget(self.skipButton, 5, 2, 1, 2)
		self.layout.addWidget(self.goodLabel, 7, 0, 1, 2)
		self.layout.addWidget(self.badLabel, 7, 2, 1, 2)
		# self.layout.addWidget(self.closeButton, 8, 3, 1, 1)
		self.actualword = ""
		self.polishword = ""
		self.createRadioButtons()
		self.loadData()

	def createRadioButtons(self):
		i = 0
		j = 0
		for file in sorted(listdir("vocabulary")):
			r = QRadioButton(file)
			r.clicked.connect(self.loadData)
			if not i and not j:
				r.setChecked(True)
			self.layout.addWidget(r, j, i, 1, 1)
			self.radioButtons[file] = r
			i += 1
			if i > 3:
				j += 1
				i = 0
		self.all = QRadioButton("All")
		self.all.clicked.connect(self.loadData)
		self.layout.addWidget(self.all, j, i, 1, 1)

	def loadData(self):
		if self.all.isChecked():
			self.data = {}
			for filename in self.radioButtons:
				with open("vocabulary/%s" % filename, "r") as file:
					lines = file.readlines()
					for line in lines:
						x = line.replace("\n", "").split(";")
						self.data[x[0]] = x[1].split("/")
		else:
			for filename in self.radioButtons:
				radio = self.radioButtons[filename]
				if radio.isChecked():
					self.data = {}
					with open("vocabulary/%s" % filename, "r") as file:
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
