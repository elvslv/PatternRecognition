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
import numpy as np

class ECDF:
	def __init__(self, observations):
		"Parameters: observations is a NumPy array."
		self.observations = np.array(observations)

	def __call__(self, x): 
		try:
			return (self.observations <= x).mean()
		except AttributeError:
			# self.observations probably needs to be converted to
			# a NumPy array
			self.observations = np.array(self.observations)
			return (self.observations <= x).mean()

	def count(self, a=None, b=None, num = 100): 
		if a == None:
			# Set up a reasonable default
			a = self.observations.min() - self.observations.std()
		if b == None:
			# Set up a reasonable default
			b = self.observations.max() + self.observations.std()
		X = np.linspace(a, b, num)
		f = np.vectorize(self.__call__)
		return X, f(X)

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
	def plot(self, x, y):
		self.axes.plot(x, y)
		self.draw()
		
	def hist(self, x, b = 28):
		self.axes.hist(x, bins = b)
		self.draw()

class labThread2(Thread):
	def __init__ (self, parent, run):
		Thread.__init__(self)
		self.parent = parent
		self.run = run

class Lab2(Labs_):
	generatedSignal = QtCore.pyqtSignal()
	analyzedSignal = QtCore.pyqtSignal()
	def __init__(self, parent):
		super(Lab2, self).__init__(parent, 1)
		self.parent = parent

		self.verticalLayout = QtGui.QVBoxLayout(self)
		self.setLayout(self.verticalLayout)
		
		self.sc1 = MyStaticMplCanvas(self, width=28, height=1000, dpi=100)
		self.sc2 = MyStaticMplCanvas(self, width=28, height=1000, dpi=100)
		
		tabWidget = QtGui.QTabWidget(self)
		self.verticalLayout.addWidget(tabWidget)
		tabWidget.addTab(self.sc1, u'Функция распределения')
		tabWidget.addTab(self.sc2, u'Гистограмма')
		
		self.subtasksComboBox = QtGui.QComboBox(self)
		self.verticalLayout.addWidget(self.subtasksComboBox)
		
		items = [u'1', u'2']
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
		self.source.currentIndexChanged.connect(self.changeControlsVisibility)
		
		self.selectFile = QtGui.QPushButton(self)
		self.selectFile.setText(u'Выбрать файл')
		self.solLayout.addWidget(self.selectFile, 1, 0)
		self.selectFile.clicked.connect(self.selectFilePressed)
		
		label = QtGui.QLabel(u'Количество элементов выборки')
		self.solLayout.addWidget(label, 2, 0)
		self.expNum = QtGui.QSpinBox(self)
		self.solLayout.addWidget(self.expNum, 2, 1)
		self.expNum.setRange(1, 1000000000)
		self.expNum.setValue(1000000)
		
		self.gen = [[label, self.expNum]]
		
		label = QtGui.QLabel(u'Не сохранять в файл')
		self.solLayout.addWidget(label, 3, 0)
		self.dontSave = QtGui.QCheckBox(self)
		self.solLayout.addWidget(self.dontSave, 3, 1)
		btn = QtGui.QPushButton(self)
		btn.setText(u'Сгенерировать выборку')
		btn.clicked.connect(self.generate)
		self.solLayout.addWidget(btn, 4, 0)
		self.isGeneratedLabel = QtGui.QLabel(u'Выборка не сгенерирована')
		self.solLayout.addWidget(self.isGeneratedLabel, 4, 1)
		self.isGenerated = False
		self.gen[0].extend([label, self.dontSave, btn, self.isGeneratedLabel])	

		self.calc = QtGui.QPushButton(self)
		self.calc.setText(u'Анализировать выборку')
		self.calc.clicked.connect(self.count)
		self.solLayout.addWidget(self.calc, 5, 0)
		self.generatedSignal.connect(self.generated)
		self.analyzedSignal.connect(self.analyzed)
		
		self.answers = [[13.5, 24.75, 0, -0.40808], [0, 0.5, 0, 0]]
		
		self.results = [[] for i in range(4)]
		
		self.labels1 = [u'Теоретический результат', u'Экспериментальный результат', u'Разница']
		self.labels2 = [u'Мат. ожидание', u'Дисперсия', u'Асимметрия', u'Эксцесс']
		
		for i, l in enumerate(self.labels1):
			label = QtGui.QLabel(l)
			self.solLayout.addWidget(label, 0, 3 + i)
			
		for i, l in enumerate(self.labels2):
			label = QtGui.QLabel(l)
			self.solLayout.addWidget(label, 1 + i, 2)
			
		for i in range(len(self.labels2)):
			self.results.append([])
			for j in range(len(self.labels1)):
				self.results[i].append(QtGui.QLineEdit(self))
				self.results[i][j].setReadOnly(True)
				self.solLayout.addWidget(self.results[i][j], 1 + i, 3 + j)
				if not j:
					self.results[i][j].setText(str(self.answers[0][i]))

		self.changeControlsVisibility()

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
		self.parent.changeState('')
		if not self.dontSave.isChecked():
			f = open('result.txt', 'w')
			f.write('%s ' %  self.expNum.value())
			for v in self.sample:
				f.write('%s ' %  v)
			f.close()

	def analyzed(self):
		self.parent.changeState('')
			
	def startGenerateDiscrete(self):
		N = self.expNum.value()
		for i in range(N):
			v = random.randint(0, 999)
			self.sample.append((v / 100) + ((v / 10) % 10) + (v % 10))
		self.generatedSignal.emit()		

	def distributionDensity(self, x):
		return pow(math.e, -x * x) / (math.sqrt(math.pi))
	
	def distributionFunction(self, x):
		return (1 + math.erf(x)) / (2 + 0.0)
	
	def startGenerateContinious(self):
		N = self.expNum.value()
		cnt = 0
		a = -10 #-2.185124219
		b = 10#2.185124219
		f_max = 1 / math.sqrt(math.pi)
		
		while(cnt < N):
			x1 = random.random()
			x2 = random.random()
			y1 = a + (b - a) * x1
			y2 = f_max * x2
			if y2 <= self.distributionDensity(y1):
				self.sample.append(y1)
				cnt += 1
				
		self.generatedSignal.emit()			
		
	def countStatParams(self, task):
		ans = [0 for i in range(4)] #m, D, gamma, k
		N = len(self.sample)
		self.graph = [0 for i in range(28)]
		for v in self.sample:
			if not task:
				self.graph[v] += 1
			ans[0] += v
		ans[0] /= (N + 0.0)
		for v in self.sample:
			ans[1] += math.pow(v - ans[0],  2)
			ans[2] += math.pow(v - ans[0],  3)
			ans[3] += math.pow(v - ans[0],  4)
		ans[1] /= (N + 0.0)
		ans[2] /= N * math.pow(ans[1], (3 + 0.0) / 2)
		ans[3] /= N * math.pow(ans[1], 2)
		ans[3] -= 3
		for i in range(4):
			self.results[i][1].setText(str(ans[i]))
			self.results[i][2].setText(str(abs(ans[i] - self.answers[task][i])))
		return self.graph
		
	def startAnalyzeDescrete(self):
		self.graph = self.countStatParams(0)
		sum = 0
		res = [0 for i in range(28)]
		for i in range(28):
			sum += (self.graph[i] + 0.0) / N
			res[i] = sum
		self.sc2.hist(self.sample)
		self.sc1.plot([i for i in range(28)], res)	
					
		self.analyzedSignal.emit()			

	def startAnalyzeContinious(self):
		self.countStatParams(1)
		self.sc2.hist(self.sample, 100) #must be optional!!!
		F = ECDF(self.sample)
		x, f = F.count()
		self.sc1.plot(x, f)	
					
		self.analyzedSignal.emit()		
		
	def generate(self):
		self.isGeneratedLabel.setText(u'Выборка не сгенерирована')
		self.isGenerated = False
		self.sample = []
		self.parent.changeState(u'Выполняется...')
		thread = labThread2(self, self.startGenerateDiscrete if not self.subtasksComboBox.currentIndex() else self.startGenerateContinious)
		thread.start()

	def changeControlsVisibility(self):
		i = self.source.currentIndex()
		for item in self.gen[0]:
			item.setVisible(not i)
		self.selectFile.setVisible(i)
		
		#for i in range(self.solLayout.count()):
		#	self.solLayout.itemAt(i).widget().setVisible(visible)

	def count(self):
		self.parent.changeState(u'Анализируется...')
		thread = labThread2(self, self.startAnalyzeDescrete if not self.subtasksComboBox.currentIndex() else self.startAnalyzeContinious)
		thread.start()


	@QtCore.pyqtSlot(int)
	def comboboxChanged(self, index):
		task = self.subtasksComboBox.currentIndex()
		for i in range(len(self.labels2)):
			for j in range(len(self.labels1)):
					self.results[i][j].setText(str(self.answers[task][i] if not j else 0))