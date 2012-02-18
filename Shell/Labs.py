#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class Labs_(QtGui.QWidget):
	def __init__(self, parent, num):
		super(Labs_, self).__init__(parent)

		self.labNum = num


class Lab1(Labs_):
	def __init__(self, parent):
		super(Lab1, self).__init__(parent, 1)

		self.verticalLayout = QtGui.QVBoxLayout(self)
		self.setLayout(self.verticalLayout)

		self.taskDescription = QtGui.QTextBrowser(self)
		self.taskDescription.setSource(QtCore.QUrl("TaskDescription1.html"))
		self.verticalLayout.addWidget(self.taskDescription)

		self.subtasksComboBox = QtGui.QComboBox(self)
		self.verticalLayout.addWidget(self.subtasksComboBox)
		
		items = [u'Выберите подзадачу', u'1.a', u'1.б', u'1.в', u'1.г', u'2']
		answers = [0.504, 0.432, 0.036, 0.027]
		for item in items:
			self.subtasksComboBox.addItem(item)
			
		self.subtasksComboBox.currentIndexChanged.connect(self.comboboxChanged)

		self.solLayout = QtGui.QGridLayout(self)
		self.verticalLayout.addLayout(self.solLayout)

		fields = [
					[u'Количество опытов', 'expNum'],
					[u'Экспериментальная вероятность', 'expProb'],
					[u'Теоретическая вероятность', 'theorProb'],
					[u'Модуль разности', 'eps']
				]
		row = 0
		for row, field in enumerate(fields):
			label = QtGui.QLabel(field[0])
			self.solLayout.addWidget(label, row, 0)
			setattr(self, field[1], QtGui.QSpinBox(self))
			self.solLayout.addWidget(getattr(self, field[1]), row, 1)

		self.calc = QtGui.QPushButton(self)
		self.calc.setText(u'Выполнить')
		self.solLayout.addWidget(self.calc, row + 1, 0)

	@QtCore.pyqtSlot(int)
	def comboboxChanged(self, index):
		if not index:
			return
		if index == 1:
			self.firstSubTask()
		
		
