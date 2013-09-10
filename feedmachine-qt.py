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
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from FeedMachine import core
from FeedMachine import scripts
from FeedMachine import config
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MainWidget(QMainWindow):

	def __init__(self, feedDB=None, parent=None):
		super(MainWidget, self).__init__(
			parent,
			windowTitle='FeedMachine',
			windowIcon=QIcon('images/feedMachine.png'),
			geometry=QRect(300, 300, 600, 372))

		self.feedDB = feedDB

		# Actions

		self.databaseNewAction = QAction(
			QIcon("images/databaseAdd.png"), 
			"&New database", self,
			statusTip="Create a new database")
		self.databaseNewAction.triggered.connect(self.databaseNew)
		self.databaseNewAction.triggered.connect(self.feedTableWidgetUpdate)
		self.databaseNewAction.triggered.connect(self.scriptTableWidgetUpdate)
		self.databaseNewAction.triggered.connect(self.actionsUpdate)

		self.databaseOpenAction = QAction(
			QIcon("images/databaseOpen.png"), 
			"&Open database", self,
			statusTip="Open a database")
		self.databaseOpenAction.triggered.connect(self.databaseOpen)
		self.databaseOpenAction.triggered.connect(self.feedTableWidgetUpdate)
		self.databaseOpenAction.triggered.connect(self.scriptTableWidgetUpdate)
		self.databaseOpenAction.triggered.connect(self.actionsUpdate)

		self.databaseSaveAction = QAction(
			QIcon("images/databaseSave.png"), 
			"Save database", self,
			statusTip="Save the open database",
			triggered=self.databaseSave)

		self.feedAddAction = QAction(
			QIcon("images/add.png"), 
			"&Add Feed", self,
			statusTip="Add a feed to the database")
		self.feedAddAction.triggered.connect(self.feedAdd)
		self.feedAddAction.triggered.connect(self.feedTableWidgetUpdate)

		self.feedUpdateAllAction = QAction(
			QIcon("images/update.png"), 
			"&Update All", self,
			statusTip="Update all feeds")
		self.feedUpdateAllAction.triggered.connect(self.feedUpdateAll)
		self.feedUpdateAllAction.triggered.connect(self.feedTableWidgetUpdate)

		self.feedUpdateAction = QAction(
			QIcon("images/update.png"), 
			"Update", self,
			statusTip="Update feed")
		self.feedUpdateAction.triggered.connect(self.feedUpdate)
		self.feedUpdateAction.triggered.connect(self.feedTableWidgetUpdate)

		self.feedRemoveAction = QAction(
			QIcon("images/remove.png"), 
			"Remove feed", self,
			statusTip="Remove feed from the database")
		self.feedRemoveAction.triggered.connect(self.feedRemove)
		self.feedRemoveAction.triggered.connect(self.feedTableWidgetUpdate)
		self.feedRemoveAction.triggered.connect(self.scriptTableWidgetUpdate)

		self.scriptAddAction = QAction(
			QIcon("images/scriptAdd.png"), 
			"Add &Script", self,
			statusTip="Attach script to feed")
		self.scriptAddAction.triggered.connect(self.scriptAdd)
		self.scriptAddAction.triggered.connect(self.scriptTableWidgetUpdate)

		self.scriptRemoveAction = QAction(
			QIcon("images/scriptRemove.png"), 
			"Remove Script", self,
			statusTip="Dettach script from feed")
		self.scriptRemoveAction.triggered.connect(self.scriptRemove)
		self.scriptRemoveAction.triggered.connect(self.feedTableWidgetUpdate)
		self.scriptRemoveAction.triggered.connect(self.scriptTableWidgetUpdate)

		self.scriptPropertiesAction = QAction(
			QIcon("images/scriptProperties.png"), 
			"Script Properties", self,
			statusTip="Script properties")
		self.scriptPropertiesAction.triggered.connect(self.scriptProperties)

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
		self.toolBar.addAction(self.feedUpdateAllAction)

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
		actionMenu.addAction(self.feedUpdateAllAction)
		actionMenu.addAction(self.scriptPropertiesAction)

		# feedsTab 
		feedsTab = QWidget()
		self.feedsTableWidget = QTableWidget(0, 3,
			selectionBehavior = QAbstractItemView.SelectRows,
			editTriggers = QAbstractItemView.NoEditTriggers,
			itemSelectionChanged = self.actionsUpdate)
		self.feedsTableWidget.setHorizontalHeaderLabels(["title", "id", "location"])		
		self.feedsTableWidget.horizontalHeader().setStretchLastSection(True)

		# feedsTab - Layout
		feedsTabLayout = QVBoxLayout(feedsTab)
		feedsTabLayout.addWidget(self.feedsTableWidget)
		feedsTab.setLayout(feedsTabLayout)

		# scriptsTab	
		scriptsTab = QWidget()
		self.scriptsTableWidget = QTableWidget(0, 5,
			selectionBehavior = QAbstractItemView.SelectRows,
			editTriggers = QAbstractItemView.NoEditTriggers,
			itemSelectionChanged = self.actionsUpdate)
		self.scriptsTableWidget.setHorizontalHeaderLabels(["Title", "Id", "Script", "Id", "Options"])		
		self.scriptsTableWidget.horizontalHeader().setStretchLastSection(True)

		# scriptsTab - Layout	
		scriptsTabLayout = QVBoxLayout(scriptsTab)
		scriptsTabLayout.addWidget(self.scriptsTableWidget)
		scriptsTab.setLayout(scriptsTabLayout)

		# Tab Widget
		self.tabs = QTabWidget()
		self.tabs.currentChanged.connect(self.actionsUpdate)
		self.tabs.currentChanged.connect(self.feedTableWidgetUpdate)
		self.tabs.currentChanged.connect(self.scriptTableWidgetUpdate)
		self.tabs.addTab(feedsTab, "Feeds")
		self.tabs.addTab(scriptsTab, "Scripts")

		# Layout
		self.setCentralWidget(self.tabs)

		self.feedTableWidgetUpdate()
		self.scriptTableWidgetUpdate()
		self.actionsUpdate()
		self.show()

	def databaseOpen(self):
		filename = QFileDialog.getOpenFileName()
		if filename:
			self.feedDB = core.FeedDB(filename)

	def databaseNew(self):
		filename = QFileDialog.getSaveFileName()
		if filename:
			self.feedDB = core.FeedDB(filename)

	def databaseSave(self):
		pass

	def actionsUpdate(self):
		if self._databaseIsOpen():
			self.feedAddAction.setEnabled(True)
			self.feedUpdateAllAction.setEnabled(True)
			self.feedUpdateAction.setEnabled(True)
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
			self.feedUpdateAllAction.setEnabled(False)
			self.feedUpdateAction.setEnabled(False)
			self.scriptAddAction.setEnabled(False)
			self.scriptRemoveAction.setEnabled(False)
			self.scriptPropertiesAction.setEnabled(False)

	def feedTableWidgetUpdate(self):
		self.feedsTableWidget.clearContents()
		if not self.feedDB:
			return
		self.feedsTableWidget.setRowCount(len(self.feedDB))
		for row, feed in enumerate(self.feedDB.getAllFeeds()):
			idTableWidgetItem = QTableWidgetItem(str(feed.id))
			locationTableWidgetItem = QTableWidgetItem(str(feed.location))
			titleTableWidgetItem = QTableWidgetItem(str(feed.data.feed.title))
			self.feedsTableWidget.setItem(row, 0, titleTableWidgetItem)
			self.feedsTableWidget.setItem(row, 1, idTableWidgetItem)
			self.feedsTableWidget.setItem(row, 2, locationTableWidgetItem)
		for i in range(self.feedsTableWidget.columnCount()-1):
			self.feedsTableWidget.resizeColumnToContents(i)
		self.feedsTableWidget.resizeRowsToContents()

	def scriptTableWidgetUpdate(self):
		if not self.feedDB:
			return
		self.scriptsTableWidget.clearContents()
		scripts = self.feedDB.getAllScripts()
		self.scriptsTableWidget.setRowCount(len(scripts))
		for row, script in enumerate(scripts):
			feed = self.feedDB.getFeedById(script.feedId)
			scriptIdTableWidgetItem = QTableWidgetItem(str(script.id))
			scriptNameTableWidgetItem = QTableWidgetItem(str(script.name))
			feedIdTableWidgetItem = QTableWidgetItem(str(script.feedId))
			feedNameTableWidgetItem = QTableWidgetItem(str(feed.data.feed.title))
			optionsTableWidgetItem = QTableWidgetItem(str(script.getOptions()))
			self.scriptsTableWidget.setItem(row, 0, feedNameTableWidgetItem)
			self.scriptsTableWidget.setItem(row, 1, feedIdTableWidgetItem)
			self.scriptsTableWidget.setItem(row, 2, scriptNameTableWidgetItem)
			self.scriptsTableWidget.setItem(row, 3, scriptIdTableWidgetItem)
			self.scriptsTableWidget.setItem(row, 4, optionsTableWidgetItem)
		for i in range(self.scriptsTableWidget.columnCount()-1):
			self.scriptsTableWidget.resizeColumnToContents(i)
		self.scriptsTableWidget.resizeRowsToContents()

	def feedAdd(self):
		location, ok = QInputDialog.getText(self, "Add Feed", "Location")
		if ok:
			self.feedDB.addFeed(location)

	def feedRemove(self):
		ok = QMessageBox.question(self, "Remove feeds?", 
			"Are you sure you want to remove selected feeds?",
			"Remove", "Cancel")
		if ok == 0:
			for row in self._selectedFeedRows():
				feedId = self.feedsTableWidget.item(row, 1).text()
				feed = self.feedDB.getFeedById(feedId)
				self.feedDB.removeFeed(feed)

	def feedUpdate(self):
		pass

	def feedUpdateAll(self):
		if self._databaseIsOpen():
			self.feedDB.updateAndRunAll()

	def scriptAdd(self):
		dialog = ScriptAddDialog(self)
		if dialog.exec_():
			options = dialog.options
			scriptName = dialog.scriptName
			for row in self._selectedFeedRows():
				feedId = self.feedsTableWidget.item(row, 1).text()
				feed = self.feedDB.getFeedById(feedId)
				feed.attachScript(scriptName, options)

	def scriptRemove(self):
		ok = QMessageBox.question(self, "Remove Scripts?", 
			"Are you sure you want to remove selected scripts?",
			"Remove", "Cancel")
		if ok == 0:
			for row in self._selectedScriptRows():
				script_id = self.scriptsTableWidget.item(row, 3).text()
				self.feedDB.removeScriptById(script_id)

	def scriptProperties(self):
		for row in self._selectedScriptRows():
			scriptId = self.scriptsTableWidget.item(row, 3).text()
			script = self.feedDB.getScriptById(scriptId)
			dialog = ScriptPropertiesDialog(script)
			dialog.exec_()

	def _selectedFeedRows(self):
		selectedModelIndexes = \
			self.feedsTableWidget.selectionModel().selectedRows()
		for index in selectedModelIndexes:
			yield index.row()

	def _selectedScriptRows(self):
		selectedModelIndexes = \
			self.scriptsTableWidget.selectionModel().selectedRows()
		for index in selectedModelIndexes:
			yield index.row()

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
	def __init__(self, parent=None):
		super(ScriptAddDialog, self).__init__(
			parent,
			windowTitle="Add Script")

		# ComboBox
		self.comboBox = QComboBox(
			self, activated=self.changeScript)
		for scriptName in config.installedScripts:
			self.comboBox.addItem(scriptName)

		# Form
		self.form = QFormLayout()
		self.form.addRow(self.comboBox)

		# ButtonBox
		buttonBox = QDialogButtonBox(
			QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
			accepted=self.accept, rejected=self.reject)

		# Layout
		self.mainLayout = QVBoxLayout()
		self.mainLayout.addLayout(self.form)
		self.mainLayout.addWidget(buttonBox)
		self.setLayout(self.mainLayout)

		self.comboBox.activated.emit(0)

	def changeScript(self, index):
		self.scriptName = self.comboBox.currentText()
		self.script = config.installedScripts[self.scriptName]
		self.options = self.script._default_options.copy()
		self.removeAllOptionWidgets()
		self.createAllOptionWidgets()

	def createAllOptionWidgets(self):
		for key in self.options:
			# Create widgets
			lineEdit = QLineEdit(textChanged=self.changedOption)
			if self.options[key]:
				lineEdit.setText(str(self.options[key]))
			# Create layout
			self.form.addRow(key, lineEdit)

	def removeAllOptionWidgets(self):
		rowCount = self.form.rowCount()
		for i in range(1, rowCount):
			self.form.itemAt(i).deleteLater()

	def changedOption(self, newText):
		lineEdit = self.sender()
		label = self.form.labelForField(lineEdit)
		key = label.text()
		text = lineEdit.text()
		self.options[key] = text

class ScriptPropertiesDialog(QDialog):
	def __init__(self, script, parent=None):
		super(ScriptPropertiesDialog, self).__init__(
			parent,
			windowTitle="Script Properties")

		# Form
		form = QFormLayout()
		form.addRow("Script", QLabel(script.name))

		# Add each option to the form
		for option in script.options:
			lineEdit = QLineEdit()
			lineEdit.setText(str(option.value))
			lineEdit.setReadOnly(True)
			form.addRow(option.name, lineEdit)

		# Create the button box
		buttonBox = QDialogButtonBox(
			QDialogButtonBox.Ok,
			accepted=self.accept)

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


