global NUM_OF_LABS;
NUM_OF_LABS = 1;

def showMessage(title, message):
	mbox = QtGui.QMessageBox(QtGui.QMessageBox.Critical, title,
		message, QtGui.QMessageBox.Ok)
	mbox.exec_()
