#-*- coding: utf-8 -*-
import sys
import os
from Misc import *
from Labs import*
from Labs2 import*
from Labs3 import *

from PyQt4 import QtGui, QtCore

from design_files.main_window import Ui_MainWindow
from design_files.dialog_about import Ui_AboutDialog

class MainApplication(QtGui.QApplication):
	def exec_(self):
		self.mainWindow = MainWindow()
		self.mainWindow.showNormal()
		try:
			super(MainApplication, self).exec_()
		except Exception, e:
			showMessage(e)

app = MainApplication(sys.argv)

class AboutDialog(QtGui.QDialog):
	def __init__(self, parent):
		super(AboutDialog, self).__init__(parent)

		self.ui = Ui_AboutDialog()
		self.ui.setupUi(self)

class MainWindow(QtGui.QMainWindow):
	def showLabTrigger(self, num):
		return lambda: self.showLab(num)
		
	def __init__(self):
		super(MainWindow, self).__init__()

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.aboutDialog = AboutDialog(self)

		self.ui.actionAbout.triggered.connect(self.aboutDialog.open)
		self.ui.tabWidget.tabCloseRequested.connect(self.closeTab)
		self.ui.tabWidget.removeTab(0)
		self.ui.tabWidget.removeTab(0)
		
		for i in range(NUM_OF_LABS):
			getattr(self.ui, 'actionLab%s' % (i + 1)).triggered.connect(self.showLabTrigger(i + 1))

	def showLab(self, num):
		for i in range(self.ui.tabWidget.count()):
			widget = self.ui.tabWidget.widget(i)
			if widget.labNum == num:
				self.ui.tabWidget.setCurrentIndex(i)
				return

		lab = globals()["Lab%s" % num](self);
		self.ui.tabWidget.addTab(lab, u'Лабораторная работа №%s' % num)
		self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

	@QtCore.pyqtSlot(int)
	def closeTab(self, index):
		self.ui.tabWidget.removeTab(index)

	def changeState(self, state):
		self.ui.statusLabel.setText(state)

if __name__ == '__main__':
	sys.exit(app.exec_())


