from PyQt4 import QtGui, QtCore

global NUM_OF_LABS;
NUM_OF_LABS = 2;

def showMessage(title, message):
	mbox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, title,
		message, QtGui.QMessageBox.Ok)
	mbox.exec_()
