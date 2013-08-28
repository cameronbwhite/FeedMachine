#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from core import *

class MainWidget(QMainWindow):

	def __init__(self, feedDB=None, parent=None):
		super(MainWidget, self).__init__(parent)

		self.feedDB = feedDB

		self.initUI()

	def initUI(self):

		self.setWindowTitle('FeedMachine')
		self.setWindowIcon(QIcon('web.png'))

		# Actions
		databaseNewAction = QAction(QIcon("images/databaseAdd.png"), "&New database", self)
		databaseOpenAction = QAction(QIcon("images/databaseOpen.png"), "&Open database", self)
		feedAddAction = QAction(QIcon("images/add.png"), "&Add Feed", self)
		feedRefreshAllAction = QAction(QIcon("images/refresh.png"), "&Refresh All", self)
		feedRefreshAction = QAction(QIcon("images/refresh.png"), "Refresh", self)
		feedRemoveAction = QAction(QIcon("images/remove.png"), "Remove feed", self)
		pluginAddAction = QAction(QIcon("images/pluginAdd.png"), "Add &Plugin", self)

		# ToolBar
		self.toolBar = self.addToolBar('Main')
		self.toolBar.addAction(databaseOpenAction)
		self.toolBar.addAction(databaseNewAction)
		self.toolBar.addSeparator()
		self.toolBar.addAction(feedAddAction)
		self.toolBar.addAction(feedRefreshAllAction)

		# Menu
		menuBar = self.menuBar()
		fileMenu = 	menuBar.addMenu('&File')
		actionMenu = menuBar.addMenu('&Action')
		fileMenu.addAction(databaseNewAction)	
		fileMenu.addAction(databaseOpenAction)
		actionMenu.addAction(feedAddAction)
		actionMenu.addAction(feedRefreshAllAction)

		# feedsTab 
		feedsTab = QWidget()
		self.feedsTableView = QTableView()
		self.feedsTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.feedsTableView.setSelectionMode(QAbstractItemView.SingleSelection)

		# feedsTab - Layout
		feedsTabLayout = QVBoxLayout(feedsTab)
		feedsTabLayout.addWidget(self.feedsTableView)
		feedsTab.setLayout(feedsTabLayout)

		# pluginsTab	
		pluginsTab = QWidget()
		self.pluginsTableView = QTableView()
		self.pluginsTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.pluginsTableView.setSelectionMode(QAbstractItemView.SingleSelection)

		# pluginsTab - Layout	
		pluginsTabLayout = QVBoxLayout(pluginsTab)
		pluginsTabLayout.addWidget(self.pluginsTableView)
		pluginsTab.setLayout(pluginsTabLayout)

		# Tabs
		self.tabs = QTabWidget()
		self.tabs.addTab(feedsTab, "Feeds")
		self.tabs.addTab(pluginsTab, "Plugins")

		# Layout
		self.setCentralWidget(self.tabs)
		self.setGeometry(300, 300, 250, 150)

		# Signals
		self.connect(databaseNewAction, SIGNAL("triggered()"), self.dbNew)
		self.connect(databaseOpenAction, SIGNAL("triggered()"), self.dbOpen)
		self.connect(feedAddAction, SIGNAL("triggered()"), self.feedAdd)
		self.connect(feedRefreshAllAction, SIGNAL("triggered()"), self.feedRefreshAll)

		#self.tableViewUpdate()
		self.show()


	def tableViewUpdate(self):
		try:
			for feed in self.feedDB:
				print(feed['location'])
				self.tableView.append(feed['location'])
		except:
			pass

	def feedAdd(self):
		if self._assertOpenDatabase():
			location = QInputDialog.getText(self, "Add Feed", "Location")
			if location:
				pass

	def feedRefreshAll(self):
		pass

	def dbOpen(self):
		filename = QFileDialog.getOpenFileName()
		if filename:
			self.feedDB = feedDB(filename)

	def dbNew(self):
		filename = QFileDialog.getSaveFileName()
		if filename:
			print(filename)
			self.feedDB = FeedDB(filename)

	def _assertOpenDatabase(self):
		if not self.feedDB:
			QMessageBox.warning(self, "No Open Database",
				"Open or create a database to continue.", 
				"Ok")
			return False
		else:
			return True


class FeedPropertiesWidget(QWidget):
	pass

#class AddFeedDialog(QDialog):
#	def __init__(self, location="", parent=None):
#		super(AddFeedDialog, self).__init__(parent)
#
#		self.location = location
#
#		locationLabel = QLabel("Feed &Location")		
#		self.locationEdit = QLineEdit()
#		self.locationEdit.setText(self.location)
#		locationLabel.setBuddy(self.locationEdit)
#
#		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
#									 QDialogButtonBox.Cancel)
#		buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
#
#		grid = QGridLayout()
#		grid.addWidget(locationLabel, 0, 0)
#		grid.addWidget(self.locationEdit, 0, 1)
#		grid.addWidget(buttonBox, 1, 0, 1, 5)
#		self.setLayout(grid)
#
#		self.connect(buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
#		self.connect(buttonBox, SIGNAL("reject()"), self, SLOT("reject()"))
#
#		self.setWindowTitle("Add Feed")


class RemoveFeedDialog(QDialog):
	def __init__(self, parent=None):
		super(RemoveFeedDialog, self).__init__(parent)

class AddScriptDialog(QDialog):
	def __init__(self, parent=None):
		super(AddScriptDialog, self).__init__(parent)


def main():

	app = QApplication(sys.argv)
	ex = MainWidget()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()


