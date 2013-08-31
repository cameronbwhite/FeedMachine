# Copyright (C) 2013, Cameron White
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the project nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE PROJECT AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE PROJECT OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
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
		self.databaseNewAction = QAction(QIcon("images/databaseAdd.png"), "&New database", self)
		self.databaseNewAction.setToolTip("Create a new database")
		self.databaseOpenAction = QAction(QIcon("images/databaseOpen.png"), "&Open database", self)
		self.databaseOpenAction.setToolTip("Open a database")
		self.databaseSaveAction = QAction(QIcon("images/databaseSave.png"), "Save database", self)
		self.databaseSaveAction.setToolTip("Save the open database")
		self.feedAddAction = QAction(QIcon("images/add.png"), "&Add Feed", self)
		self.feedAddAction.setToolTip("Add a new feed to the self.database")
		self.feedRefreshAllAction = QAction(QIcon("images/refresh.png"), "&Refresh All", self)
		self.feedRefreshAllAction.setToolTip("Refresh all the feeds in the self.database")
		self.feedRefreshAction = QAction(QIcon("images/refresh.png"), "Refresh", self)
		self.feedRefreshAction.setToolTip("Refresh feed")
		self.feedRemoveAction = QAction(QIcon("images/remove.png"), "Remove feed", self)
		self.feedRemoveAction.setToolTip("Remove feed from self.database")
		self.scriptAddAction = QAction(QIcon("images/scriptAdd.png"), "Add &Script", self)
		self.scriptAddAction.setToolTip("Attach script to feed")
		self.scriptRemoveAction = QAction(QIcon("images/scriptRemove.png"), "Remove Script", self)
		self.scriptRemoveAction.setToolTip("Remove script from feed")

		# ToolBar
		self.toolBar = self.addToolBar('Main')
		self.toolBar.setMovable(False)
		self.toolBar.addAction(self.databaseOpenAction)
		self.toolBar.addAction(self.databaseNewAction)
		self.toolBar.addAction(self.databaseSaveAction)
		self.toolBar.addAction(self.feedAddAction)
		self.toolBar.addAction(self.feedRemoveAction)
		self.toolBar.addAction(self.scriptAddAction)
		self.toolBar.addAction(self.scriptRemoveAction)
		self.toolBar.addAction(self.feedRefreshAllAction)

		# Menu
		menuBar = self.menuBar()
		fileMenu = menuBar.addMenu('&File')
		actionMenu = menuBar.addMenu('&Action')
		fileMenu.addAction(self.databaseNewAction)	
		fileMenu.addAction(self.databaseOpenAction)
		fileMenu.addAction(self.databaseSaveAction)
		actionMenu.addAction(self.feedAddAction)
		actionMenu.addAction(self.feedRemoveAction)
		actionMenu.addAction(self.scriptAddAction)
		actionMenu.addAction(self.scriptRemoveAction)
		actionMenu.addAction(self.feedRefreshAllAction)

		# feedsTab 
		feedsTab = QWidget()
		self.feedsTableWidget = QTableWidget(0, 3)
		self.feedsTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.feedsTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.feedsTableWidget.setHorizontalHeaderLabels(["id", "title", "location"])		
		self.feedsTableWidget.horizontalHeader().setStretchLastSection(True)

		# feedsTab - Layout
		feedsTabLayout = QVBoxLayout(feedsTab)
		feedsTabLayout.addWidget(self.feedsTableWidget)
		feedsTab.setLayout(feedsTabLayout)

		# scriptsTab	
		scriptsTab = QWidget()
		self.scriptsTableWidget = QTableWidget(0, 5)
		self.scriptsTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.scriptsTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.scriptsTableWidget.setHorizontalHeaderLabels(["Feed Id", "Title", "Script Id", "Script", "Options"])		
		self.scriptsTableWidget.horizontalHeader().setStretchLastSection(True)

		# scriptsTab - Layout	
		scriptsTabLayout = QVBoxLayout(scriptsTab)
		scriptsTabLayout.addWidget(self.scriptsTableWidget)
		scriptsTab.setLayout(scriptsTabLayout)

		# Tabs
		self.tabs = QTabWidget()
		self.tabs.addTab(feedsTab, "Feeds")
		self.tabs.addTab(scriptsTab, "Scripts")

		# Layout
		self.setCentralWidget(self.tabs)
		self.setGeometry(300, 300, 600, 372)

		# Signals
		self.connect(self.databaseNewAction, SIGNAL("triggered()"), self.databaseNew)
		self.connect(self.databaseOpenAction, SIGNAL("triggered()"), self.databaseOpen)
		self.connect(self.databaseSaveAction, SIGNAL("triggered()"), self.databaseSave)
		self.connect(self.feedAddAction, SIGNAL("triggered()"), self.feedAdd)
		self.connect(self.feedRemoveAction, SIGNAL("triggered()"), self.feedRemove)
		self.connect(self.feedRefreshAllAction, SIGNAL("triggered()"), self.feedRefreshAll)
		self.connect(self.feedsTableWidget, SIGNAL("itemSelectionChanged()"), self.updateUI)
		self.connect(self.tabs, SIGNAL("currentChanged(int)"), self.updateUI)

		self.tableWidgetUpdate()
		self.updateUI()
		self.show()

	def updateUI(self):
		if self._databaseIsOpen():
			self.feedAddAction.setEnabled(True)
			self.feedRefreshAllAction.setEnabled(True)
			self.feedRefreshAction.setEnabled(True)
			self.databaseSaveAction.setEnabled(True)
			if self._onFeedsTab() and self._isAFeedSelected():
				self.scriptAddAction.setEnabled(True)
				self.feedRemoveAction.setEnabled(True)
			else:
				self.scriptAddAction.setEnabled(False)
				self.feedRemoveAction.setEnabled(False)
			if self._onScriptsTab() and self._isAScriptSelected():
				self.scriptRemoveAction.setEnabled(True)
			else:
				self.scriptRemoveAction.setEnabled(False)
		else:
			self.databaseSaveAction.setEnabled(False)
			self.feedRemoveAction.setEnabled(False)
			self.feedAddAction.setEnabled(False)
			self.feedRemoveAction.setEnabled(False)
			self.feedRefreshAllAction.setEnabled(False)
			self.feedRefreshAction.setEnabled(False)
			self.scriptAddAction.setEnabled(False)
			self.scriptRemoveAction.setEnabled(False)

	def tableWidgetUpdate(self):
		self.feedsTableWidget.clearContents()
		try:
			self.feedsTableWidget.setRowCount(len(self.feedDB))
			for row, feed in enumerate(self.feedDB):
				idTableWidgetItem = QTableWidgetItem(str(feed['feed_id']))
				locationTableWidgetItem = QTableWidgetItem(feed['location'])
				titleTableWidgetItem = QTableWidgetItem(feed['feed'].feed.title)
				self.feedsTableWidget.setItem(row, 0, idTableWidgetItem)
				self.feedsTableWidget.setItem(row, 1, titleTableWidgetItem)
				self.feedsTableWidget.setItem(row, 2, locationTableWidgetItem)
		except TypeError as e:
			print(e)

	def feedAdd(self):
		location, ok = QInputDialog.getText(self, "Add Feed", "Location")
		if ok:
			self.feedDB.add_feed(location)
			self.tableWidgetUpdate()	
			self.updateUI()

	def feedRemove(self):
		ok = QMessageBox.question(self, "Remove feeds?", 
			"Are you sure you want to remove selected feeds?",
			"Remove", "Cancel")
		if ok == 0:
			selectedModelIndexes = self.feedsTableWidget.selectionModel().selectedRows()
			for index in selectedModelIndexes:
				row = index.row()
				feed_id = self.feedsTableWidget.item(row, 0).text()
				print(feed_id)
				self.feedDB.remove_feed_by_id(feed_id)
			self.tableWidgetUpdate()	
			self.updateUI()


	def feedRefreshAll(self):
		if self._databaseIsOpen():
			self.feedDB.update_all_feeds()


	def databaseOpen(self):
		filename = QFileDialog.getOpenFileName()
		if filename:
			self.feedDB = FeedDB(filename)
			self.tableWidgetUpdate()	
			self.updateUI()

	def databaseNew(self):
		filename = QFileDialog.getSaveFileName()
		if filename:
			self.feedDB = FeedDB(filename)
			self.tableWidgetUpdate()	
			self.updateUI()

	def databaseSave(self):
		pass

	def _databaseIsOpen(self):
		if self.feedDB is None:
			return False
		else:
			return True

	def _onFeedsTab(self):
		if self.tabs.currentIndex() == 0:
			return True
		else:
			return False

	def _onScriptsTab(self):
		if self.tabs.currentIndex() == 1:
			return True
		else:
			return False

	def _isAFeedSelected(self):
		if len(self.feedsTableWidget.selectedItems()) > 0:
			return True
		else:
			return False

	def _isAScriptSelected(self):
		return False

class FeedPropertiesWidget(QWidget):
	pass

class RemoveFeedDialog(QDialog):
	def __init__(self, parent=None):
		super(RemoveFeedDialog, self).__init__(parent)

class AddScriptDialog(QDialog):
	def __init__(self, feedDB, parent=None):
		super(AddScriptDialog, self).__init__(parent)

		self.feedDB = feedDB


def main():

	app = QApplication(sys.argv)
	ex = MainWidget()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()


