#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import random, math
import os.path
import os
from threading import Thread
from Misc import *
from Labs import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pylab
class MyMplCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
# We want the axes cleared every time plot() is called
		self.axes.hold(False)
		FigureCanvas.__init__(self, fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
		                           QtGui.QSizePolicy.Expanding,
		                           QtGui.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

class MyStaticMplCanvas(MyMplCanvas):
	def plot_(self, x, y):
		self.axes.plot(x, y)
		self.draw()

class labThread2(Thread):
	def __init__ (self, lab):
		Thread.__init__(self)
		self.expNum = lab.expNum.value()
		self.lab = lab

	def run(self):
		self.lab.parent.changeState(u'Выполняется...')
		cnt = 0
		for i in range(self.expNum):
			self.lab.sample.append(random.randint(0, 999))
		self.lab.parent.changeState('')
		self.lab.generatedSignal.emit()

class Lab2(Labs_):
	generatedSignal = QtCore.pyqtSignal()
	def __init__(self, parent):
		super(Lab2, self).__init__(parent, 1)
		self.parent = parent

		self.verticalLayout = QtGui.QVBoxLayout(self)
		self.setLayout(self.verticalLayout)

        	self.sc = MyStaticMplCanvas(self, width=28, height=1000, dpi=100)
		self.verticalLayout.addWidget(self.sc)
		
		self.subtasksComboBox = QtGui.QComboBox(self)
		self.verticalLayout.addWidget(self.subtasksComboBox)
		
		items = [u'Выберите подзадачу', u'1', u'2']
		for item in items:
			self.subtasksComboBox.addItem(item)
			
		self.subtasksComboBox.currentIndexChanged.connect(self.comboboxChanged)

		layout = QtGui.QVBoxLayout(self)
		self.verticalLayout.addLayout(layout)
		
		self.solLayout = QtGui.QGridLayout(self)
		layout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		layout.addLayout(self.solLayout)
		
		label = QtGui.QLabel(u'Источник выборки')
		self.solLayout.addWidget(label, 0, 0)
		self.source = QtGui.QComboBox(self)
		self.solLayout.addWidget(self.source, 0, 1)
		self.source.addItems([u'Сгенерировать выборку', u'Загрузить из файла'])
		
		label = QtGui.QLabel(u'Количество элементов выборки')
		self.solLayout.addWidget(label, 1, 0)
		self.expNum = QtGui.QSpinBox(self)
		self.solLayout.addWidget(self.expNum, 1, 1)
		self.expNum.setRange(1, 1000000000)
		self.expNum.setValue(1000000)
		
		self.gen = [[label, self.expNum]]
		
		label = QtGui.QLabel(u'Не сохранять в файл')
		self.solLayout.addWidget(label, 2, 0)
		self.dontSave = QtGui.QCheckBox(self)
		self.solLayout.addWidget(self.dontSave, 2, 1)
		btn = QtGui.QPushButton(self)
		btn.setText(u'Сгенерировать выборку')
		btn.clicked.connect(self.generate)
		self.solLayout.addWidget(btn, 3, 0)
		self.isGeneratedLabel = QtGui.QLabel(u'Выборка не сгенерирована')
		self.solLayout.addWidget(self.isGeneratedLabel, 3, 1)
		self.isGenerated = False
		self.gen[0].extend([label, self.dontSave, btn, self.isGeneratedLabel])	

		self.selectFile = QtGui.QPushButton(self)
		self.selectFile.setText(u'Выбрать файл')
		self.solLayout.addWidget(self.selectFile, 4, 0)
		self.selectFile.clicked.connect(self.selectFilePressed)
		self.calc = QtGui.QPushButton(self)
		self.calc.setText(u'Анализировать выборку')
		self.calc.clicked.connect(self.count)
		self.solLayout.addWidget(self.calc, 5, 0)
		self.generatedSignal.connect(self.generated)
		#self.changeControlsVisibility(False)

		#self.defaultValues = [[100000, 0.504], [100000, 0.432], [100000, 0.036], [100000, 0.027],  [100000, 1 - math.sqrt(3) / 2]]

	def selectFilePressed(self):
		fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',  os.getcwd())
		if os.path.isfile(fname):
			self.isGeneratedLabel.setText(u'Загружается выборка...')
			self.isGenerated = False
			self.sample = []
			try:
				f = open(fname, 'r')
				for i, val in enumerate(f.read().split()):
					v = int(val)
					assert v > 0 if not i else v >= 0 and v <= 999
					if not i:
						self.expNum.setValue(v)
					else:
						self.sample.append(v)
				f.close()
				self.isGeneratedLabel.setText(u'Выборка загружена')
			except (Exception, e):
				self.isGeneratedLabel.setText(u'Выборка не сгенерирована')
				showMessage(u'Ошибка', u'Некорректный формат файла')

	def generated(self):
		self.isGenerated = True
		self.isGeneratedLabel.setText(u'Выборка сгенерирована')
		if not self.dontSave.isChecked():
			f = open('result.txt', 'w')
			f.write('%s ' %  self.expNum.value())
			for v in self.sample:
				f.write('%s ' %  v)
			f.close()

	def generate(self):
		self.isGeneratedLabel.setText(u'Выборка не сгенерирована')
		self.isGenerated = False
		self.sample = []
		thread = labThread2(self)
		thread.start()

	def changeControlsVisibility(self, visible):
		for i in range(self.solLayout.count()):
			self.solLayout.itemAt(i).widget().setVisible(visible)

	def count(self):
		m = 0
		D = 0
		gamma = 0
		k = 0
		N = len(self.sample)
		self.graph = [0 for i in range(28)]
		for v in self.sample:
			val = (v / 100) + ((v / 10) % 10) + (v % 10)
			self.graph[val] += 1
			m += val
		m /= (N + 0.0)
		for v in self.sample:
			val = (v / 100) + ((v / 10) % 10) + (v % 10)
			D += math.pow(val - m,  2)
			gamma += math.pow(val - m,  3)
			k += math.pow(val - m,  4)
		D /= (N + 0.0)
		gamma /= N * math.pow(D, 3 / 2)
		k /= N * math.pow(D,  2)
		k -= 3
		self.sc.plot_([i for i in range(28)], self.graph)
		print m, D, gamma, k, self.graph
		
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

