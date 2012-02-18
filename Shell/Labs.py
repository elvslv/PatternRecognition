#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import random

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

		layout = QtGui.QVBoxLayout(self)
		self.verticalLayout.addLayout(layout)
		
		self.solLayout = QtGui.QGridLayout(self)
		layout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		layout.addLayout(self.solLayout)

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
			setattr(self, field[1], QtGui.QSpinBox(self) if not row else QtGui.QLineEdit(self))
			if row: 
				getattr(self, field[1]).setReadOnly(False)
			else:
				getattr(self, field[1]).setMaximum(1000000000)
			self.solLayout.addWidget(getattr(self, field[1]), row, 1)

		self.calc = QtGui.QPushButton(self)
		self.calc.setText(u'Выполнить')
		self.calc.clicked.connect(self.count)
		self.solLayout.addWidget(self.calc, row + 1, 0)

		self.changeControlsVisibility(False)

		self.defaultValues = [[1000000, 0.504], [1000000, 0.432], [1000000, 0.036], [1000000, 0.027]]

	def changeControlsVisibility(self, visible):
		for i in range(self.solLayout.count()):
			self.solLayout.itemAt(i).widget().setVisible(visible)

	def solve(self):
		self.changeControlsVisibility(True)
		self.count()

	def count(self):
		task = self.subtasksComboBox.currentIndex()
		cnt = 0
		for i in range(self.expNum.value()):
			cnt += getattr(self, 'check%s' % task)(random.randint(0, 9999))
		result  = (cnt + 0.0) / self.expNum.value()
		print result
		self.expProb.setText(str(result))
		self.eps.setText(str(abs(result - self.defaultValues[task - 1][1])))
	
	@QtCore.pyqtSlot(int)
	def comboboxChanged(self, index):
		if not index:
			self.changeControlsVisibility(False)
			return

		self.expNum.setValue(self.defaultValues[index - 1][0])
		self.theorProb.setText(str(self.defaultValues[index - 1][1]))

		if index in range(1, 5):
			self.solve()

	def getDigits(self, n):
		return [n / 1000, (n / 100) % 10, (n / 10) % 10, n % 10]

	def check1(self, n):
		a = self.getDigits(n)
		result = 0
		for i in range(4):
			for j in range(i + 1, 4):
				if a[i] == a[j]:
					result += 1
					break;
		return result == 0
		
	def check2(self, n):
		a = self.getDigits(n)
		result = 0
		for i in range(4):
			for j in range(i + 1, 4):
				if a[i] == a[j]:
					result += 1
		return result == 1
		
	def check3(self, n):
		a = self.getDigits(n)
		result = 0
		for i in range(4):
			for j in range(i + 1, 4):
				for k in range(j + 1, 4):
					if a[i] == a[j] and a[j] == a[k]:
						result += 1
						break;
		return result == 1
		
	def check4(self, n):
		a = self.getDigits(n)
		result = 0
		for i in range(4):
			for j in range(i + 1, 4):
				if a[i] == a[j]:
					for k in range(4):
						if k != i and k != j:
							if a[k] == a[6 - k - j - i]:
								result += 1
		
		return result == 4
		
		
		
