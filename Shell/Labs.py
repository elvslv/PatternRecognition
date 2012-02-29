#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import random, math
from threading import Thread

class Labs_(QtGui.QWidget):
	def __init__(self, parent, num):
		super(Labs_, self).__init__(parent)

		self.labNum = num



class labThread(Thread):
	def __init__ (self, lab, task):
		Thread.__init__(self)
		self.task = task
		self.func = getattr(lab, 'check%s' % task)
		self.expNum = lab.expNum.value()
		self.l = lab.segmentLength.value()
		self.lab = lab

	def run(self):
		self.lab.parent.changeState(u'Выполняется...')
		cnt = 0
		for i in range(self.expNum):
			cnt += self.func(random.randint(0, 9999) if self.task != 5 else random.uniform(-self.l, self.l))
		result  = (cnt + 0.0) / self.expNum
		self.lab.expProb.setText(str(result))
		self.lab.eps.setText(str(abs(result - self.lab.defaultValues[self.task - 1][1])))
		self.lab.parent.changeState('')


class Lab1(Labs_):
	def __init__(self, parent):
		super(Lab1, self).__init__(parent, 1)
		self.parent = parent

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
					[u'Количество опытов', 'expNum', int],
					[u'Радиус', 'segmentLength', float],
					[u'Экспериментальная вероятность', 'expProb', str],
					[u'Теоретическая вероятность', 'theorProb', str],
					[u'Модуль разности', 'eps', str]
				]
		row = 0
		for row, field in enumerate(fields):
			label = QtGui.QLabel(field[0])
			self.solLayout.addWidget(label, row, 0)
			if field[1] == 'segmentLength':
				self.segmentLengthLabel = label;
			obj = None
			if field[2] is int:
				obj = QtGui.QSpinBox(self)
				obj.setRange(0, 1000000000)
			elif field[2] is float:
				obj = QtGui.QDoubleSpinBox(self)
				obj.setRange(0.01, 1000000000)
			else:
				obj = QtGui.QLineEdit(self)
				obj.setReadOnly(True)
				
			setattr(self, field[1], obj)
			self.solLayout.addWidget(obj, row, 1)
			
		self.segmentLength.setValue(1)
		self.calc = QtGui.QPushButton(self)
		self.calc.setText(u'Выполнить')
		self.calc.clicked.connect(self.count)
		self.solLayout.addWidget(self.calc, row + 1, 0)

		self.changeControlsVisibility(False)

		self.defaultValues = [[100000, 0.504], [100000, 0.432], [100000, 0.036], [100000, 0.027],  [100000, 1 - math.sqrt(3) / 2]]

	def changeControlsVisibility(self, visible):
		for i in range(self.solLayout.count()):
			self.solLayout.itemAt(i).widget().setVisible(visible)

	def count(self):
		task = self.subtasksComboBox.currentIndex()
		thread = labThread(self, task)
		thread.start()
	
	@QtCore.pyqtSlot(int)
	def comboboxChanged(self, index):
		if not index:
			self.changeControlsVisibility(False)
			return

		self.expNum.setValue(self.defaultValues[index - 1][0])
		self.theorProb.setText(str(self.defaultValues[index - 1][1]))

		self.changeControlsVisibility(True)
		self.segmentLength.setVisible(index not in range(1, 5))
		self.segmentLengthLabel.setVisible(index not in range(1, 5))
		self.count()

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


	def check5(self, c):
		r = self.segmentLength.value() + 0.0
		return 4 * (r * r - c * c) <= r * r
		
		
