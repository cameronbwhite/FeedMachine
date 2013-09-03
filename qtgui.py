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
from functools import partial
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
		self.setWindowIcon(QIcon('images/feedMachine.png'))

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
		self.scriptPropertiesAction = QAction(QIcon("images/scriptProperties.png"), "Script Properties", self)
		self.scriptPropertiesAction.setToolTip("Get the script Properties")

		# ToolBar
		self.toolBar = self.addToolBar('Main')
		self.toolBar.setMovable(False)
		self.toolBar.setFloatable(False)
		self.toolBar.addAction(self.databaseOpenAction)
		self.toolBar.addAction(self.databaseNewAction)
		self.toolBar.addAction(self.databaseSaveAction)
		self.toolBar.addAction(self.feedAddAction)
		self.toolBar.addAction(self.feedRemoveAction)
		self.toolBar.addAction(self.scriptAddAction)
		self.toolBar.addAction(self.scriptRemoveAction)
		self.toolBar.addAction(self.scriptPropertiesAction)
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
		actionMenu.addAction(self.scriptPropertiesAction)

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
		self.connect(self.scriptAddAction, SIGNAL("triggered()"), self.scriptAdd)
		self.connect(self.scriptRemoveAction, SIGNAL("triggered()"), self.scriptRemove)
		self.connect(self.scriptPropertiesAction, SIGNAL("triggered()"), self.scriptProperties)
		self.connect(self.feedsTableWidget, SIGNAL("itemSelectionChanged()"), self.updateActions)
		self.connect(self.scriptsTableWidget, SIGNAL("itemSelectionChanged()"), self.updateActions)
		self.connect(self.tabs, SIGNAL("currentChanged(int)"), self.updateActions)

		self.feedTableWidgetUpdate()
		self.scriptTableWidgetUpdate()
		self.updateActions()
		self.show()

	def updateActions(self):
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
				self.scriptPropertiesAction.setEnabled(True)
			else:
				self.scriptRemoveAction.setEnabled(False)
				self.scriptPropertiesAction.setEnabled(False)
		else:
			self.databaseSaveAction.setEnabled(False)
			self.feedRemoveAction.setEnabled(False)
			self.feedAddAction.setEnabled(False)
			self.feedRemoveAction.setEnabled(False)
			self.feedRefreshAllAction.setEnabled(False)
			self.feedRefreshAction.setEnabled(False)
			self.scriptAddAction.setEnabled(False)
			self.scriptRemoveAction.setEnabled(False)
			self.scriptPropertiesAction.setEnabled(False)

	def feedTableWidgetUpdate(self):
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

	def scriptTableWidgetUpdate(self):
		self.scriptsTableWidget.clearContents()
		try:
			scripts = self.feedDB.get_all_scripts()
			self.scriptsTableWidget.setRowCount(len(scripts))
			for row, script in enumerate(scripts):
				scriptIdTableWidgetItem = QTableWidgetItem(str(script['script_id']))
				scriptNameTableWidgetItem = QTableWidgetItem(str(script['script'].__name__))
				feedIdTableWidgetItem = QTableWidgetItem(str(script['feed_id']))
				feedNameTableWidgetItem = QTableWidgetItem("TODO")
				optionsTableWidgetItem = QTableWidgetItem(str(script['options']))
				self.scriptsTableWidget.setItem(row, 0, feedIdTableWidgetItem)
				self.scriptsTableWidget.setItem(row, 1, feedNameTableWidgetItem)
				self.scriptsTableWidget.setItem(row, 2, scriptIdTableWidgetItem)
				self.scriptsTableWidget.setItem(row, 3, scriptNameTableWidgetItem)
				self.scriptsTableWidget.setItem(row, 4, optionsTableWidgetItem)
		except TypeError as e:
			print(e)
		except AttributeError as e:
			print(e)

	def feedAdd(self):
		location, ok = QInputDialog.getText(self, "Add Feed", "Location")
		if ok:
			self.feedDB.add_feed(location)
			self.feedTableWidgetUpdate()	
			self.updateActions()

	def feedRemove(self):
		ok = QMessageBox.question(self, "Remove feeds?", 
			"Are you sure you want to remove selected feeds?",
			"Remove", "Cancel")
		if ok == 0:
			selectedModelIndexes = self.feedsTableWidget.selectionModel().selectedRows()
			for index in selectedModelIndexes:
				row = index.row()
				feed_id = self.feedsTableWidget.item(row, 0).text()
				self.feedDB.remove_feed_by_id(feed_id)
			self.feedTableWidgetUpdate()	
			self.updateActions()

	def feedRefreshAll(self):
		if self._databaseIsOpen():
			self.feedDB.update_all_feeds()

	def databaseOpen(self):
		filename = QFileDialog.getOpenFileName()
		if filename:
			self.feedDB = FeedDB(filename)
			self.feedTableWidgetUpdate()	
			self.scriptTableWidgetUpdate()
			self.updateActions()

	def databaseNew(self):
		filename = QFileDialog.getSaveFileName()
		if filename:
			self.feedDB = FeedDB(filename)
			self.feedTableWidgetUpdate()	
			self.scriptTableWidgetUpdate()
			self.updateActions()

	def databaseSave(self):
		pass

	def scriptAdd(self):
		dialog = ScriptAddDialog(self.feedDB, self)
		if dialog.exec_():
			options = dialog.options
			script = dialog.script
			selectedModelIndexes = self.feedsTableWidget.selectionModel().selectedRows()
			for index in selectedModelIndexes:
				row = index.row()
				feed_id = self.feedsTableWidget.item(row, 0).text()
				self.feedDB.add_script(feed_id, script, options)
			self.feedTableWidgetUpdate()	
			self.scriptTableWidgetUpdate()
			self.updateActions()

	def scriptRemove(self):
		ok = QMessageBox.question(self, "Remove Scripts?", 
			"Are you sure you want to remove selected scripts?",
			"Remove", "Cancel")
		if ok == 0:
			selectedModelIndexes = self.scriptsTableWidget.selectionModel().selectedRows()
			for index in selectedModelIndexes:
				row = index.row()
				script_id = self.scriptsTableWidget.item(row, 2).text()
				self.feedDB.remove_script_by_id(script_id)
			self.scriptTableWidgetUpdate()	
			self.updateActions()

	def scriptProperties(self):
		selectedModelIndexes = self.scriptsTableWidget.selectionModel().selectedRows()
		for index in selectedModelIndexes:
			row = index.row()
			feed_id = self.scriptsTableWidget.item(row, 0).text()
			script_id = self.scriptsTableWidget.item(row, 2).text()
			script_name = self.scriptsTableWidget.item(row, 3).text()
			options = eval(self.scriptsTableWidget.item(row, 4).text())
			dialog = ScriptPropertiesDialog(script_name, options)
			dialog.exec_()

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
		if len(self.scriptsTableWidget.selectedItems()) > 0:
			return True
		else:
			return False

class ScriptAddDialog(QDialog):
	def __init__(self, feedDB, parent=None):
		super(ScriptAddDialog, self).__init__(parent)

		self.feedDB = feedDB
		self.optionWidgetLayouts = []
		self.optionWidgetPartials = []
		self.available_scripts = get_available_scripts()

		# ComboBox
		self.comboBox = QComboBox(self)
		for script in self.available_scripts:
			self.comboBox.addItem(script.__name__)

		# Form
		self.form = QFormLayout()
		self.form.addRow(self.comboBox)

		# ButtonBox
		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok| 
									 QDialogButtonBox.Cancel)

		# Layout
		self.mainLayout = QVBoxLayout()
		self.mainLayout.addLayout(self.form)
		self.mainLayout.addWidget(buttonBox)
		self.setLayout(self.mainLayout)

		# Signals
		self.connect(self.comboBox, SIGNAL('activated(int)'), self.changeScript)
		self.connect(buttonBox, SIGNAL('accepted()'), self, SLOT('accept()'))
		self.connect(buttonBox, SIGNAL('rejected()'), self, SLOT('reject()'))

		self.comboBox.emit(SIGNAL('activated(int)'), 0)

	def changeScript(self, index):
		currentText = self.comboBox.currentText()
		self.script = self.getScriptFromName(currentText)
		self.options = self.script._default_options.copy()
		self.removeAllOptionWidgets()
		self.createAllOptionWidgets()

	def createAllOptionWidgets(self):
		for key in self.options:
			# Create widgets
			lineEdit = QLineEdit()
			if self.options[key]:
				lineEdit.setText(str(self.options[key]))
			# Create layout
			self.form.addRow(key, lineEdit)
			# Signals
			self.connect(lineEdit, SIGNAL('textChanged(const QString&)'), self.changedOption)

	def removeAllOptionWidgets(self):
		rowCount = self.form.rowCount()
		for i in range(1, rowCount):
			self.form.itemAt(i).deleteLater()
		self.optionWidgetLayouts = []
		self.optionWidgetPartials = []

	def changedOption(self, newText):
		lineEdit = self.sender()
		label = self.form.labelForField(lineEdit)
		key = label.text()
		text = lineEdit.text()
		self.options[key] = text

	def getScriptFromName(self, name):
		for script in self.available_scripts:
			if script.__name__ == name:
				return script

class ScriptPropertiesDialog(QDialog):
	def __init__(self, scriptName, options, parent=None):
		super(ScriptPropertiesDialog, self).__init__(parent)

		# Form
		form = QFormLayout()
		form.addRow("Script", QLabel(scriptName))

		# Add each option to the form
		for i, key in enumerate(options):
			lineEdit = QLineEdit()
			lineEdit.setText(str(options[key]))
			lineEdit.setReadOnly(True)
			form.addRow(key, lineEdit)

		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)

		# Signals
		self.connect(buttonBox, SIGNAL('accepted()'), self, SLOT('accept()'))

		# Layout
		layout = QVBoxLayout()
		layout.addLayout(form)
		layout.addWidget(buttonBox)
		self.setLayout(layout)


def main():
	app = QApplication(sys.argv)
	ex = MainWidget()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()


