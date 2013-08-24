#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from feed import FeedMachine
from PyQt4 import QtGui

class MainWidget(QtGui.QWidget):

	def __init__(self, feedMachine, parent=None):
		super(FeedMachineGui, self).__init__(parent)

		assert isinstance(feedMachine, FeedMachine)
		self.feedMachine = feedMachine

		self.initUI()

	def initUI(self):

		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle('FeedMachine')
		self.setWindowIcon(QtGui.QIcon('web.png'))

		self.browser = QtGui.QTextBrowser()

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.browser)

		self.setLayout(layout)

		self.updateBrowser()
		self.show()

	def updateBrowser(self):
		for feed in self.feedMachine:
			print(feed['location'])
			self.browser.append(feed['location'])

class FeedPropertiesWidget(QtGui.QWidget):
	pass

class AddFeedDialog(QtGui.QDialog):
	pass

class RemoveFeedDialog(QtGui.QDialog):
	pass

class AddScriptDialog(QtGui.QDialog):
	pass


def main():

	app = QtGui.QApplication(sys.argv)
	ex = FeedMachineGui(FeedMachine('/tmp/feedMachine.db.1'))
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()


