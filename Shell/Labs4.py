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
from matplotlib import mlab
import pylab
import numpy as np
import numpy.linalg as linalg
#from scipy import interpolate

class labThread4(Thread):
	def __init__ (self, parent, run):
		Thread.__init__(self)
		self.parent = parent
		self.run = run

class MyMplCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=5, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(111)
		self.axes.set_autoscale_on(True)
		#self.axes.hold(False)
		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
		                           QtGui.QSizePolicy.Expanding,
		                           QtGui.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

class MyStaticMplCanvas(MyMplCanvas):
	def plot(self, x, y, ch, col):
		if ch:
			self.axes.plot(x, y, ch, zorder = 0, color = col)
		else:
			self.axes.plot(x, y, zorder = 0, color = col)
		#self.draw()
		
	def clear(self):
		self.axes.hold(False)
		self.axes.plot([], [])
		self.axes.hold(True)
		#self.draw()
		#self.axes.autoscale(enable=True, axis='both', tight=True)

	def draw_(self):
		self.draw()

	def vlines(self, x, ymin, ymax):
		print x, ymin, ymax
		self.axes.vlines(x, ymin, ymax, colors = 'blue')
		self.axes.relim()
		self.draw()
		#self.axes.autoscale(enable=True, axis='both', tight=True)

class DigitalSignal:
	def __init__(self, N):
		self.N = N;

class DigitalSignal1(DigitalSignal):
	def getDataFromLayout(self, layout):
		self.n0 = layout.itemAtPosition(0, 1).widget().value()
	
	def generate(self):
		u = [1 if i == self.n0 else 0 for i in range(self.N)]
		return u
		
	def fillLayout(self, layout):
		label = QtGui.QLabel(u'Задержка')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QSpinBox()
		layout.addWidget(spinBox, 0, 1)
		return layout

class DigitalSignal2(DigitalSignal):
	def getDataFromLayout(self, layout):
		self.n0 = layout.itemAtPosition(0, 1).widget().value()	
	
	def generate(self):
		u = [0 if i < self.n0 else 1 for i in range(self.N)]
		return u
		
	def fillLayout(self, layout):
		label = QtGui.QLabel(u'Задержка')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QSpinBox()
		layout.addWidget(spinBox, 0, 1)
		return layout

class DigitalSignal3(DigitalSignal):
	def getDataFromLayout(self, layout):
		self.a = layout.itemAtPosition(0, 1).widget().value()		
	
	def generate(self):
		u = [math.pow(self.a, i) for i in range(self.N)]
		return u

	def fillLayout(self, layout):
		label = QtGui.QLabel(u'Основание')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.setRange(0.0000000001, 0.9999999999)
		layout.addWidget(spinBox, 0, 1)
		return layout		
		
class DigitalSignal4(DigitalSignal):
	def getDataFromLayout(self, layout):
		self.a = layout.itemAtPosition(0, 1).widget().value()	
		self.omega = layout.itemAtPosition(1, 1).widget().value()
		self.phi = layout.itemAtPosition(2, 1).widget().value()		
		
	def generate(self):
		u = [self.a * math.sin(i * omega + phi) for i in range(self.N)]
		return u

	def fillLayout(self, layout):
		label = QtGui.QLabel(u'Амплитуда')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'Частота')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 1, 1)
		label = QtGui.QLabel(u'Начальная фаза')
		layout.addWidget(label, 2, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 2, 1)
		return layout				
		
class DigitalSignal5(DigitalSignal):
	def getDataFromLayout(self, layout):
		self.L = layout.itemAtPosition(0, 1).widget().value()		
	
	def generate(self):
		u = [1 if i % L < L / 2.0 else -1  for i in range(self.N)]
		return u

	def fillLayout(self, layout):
		label = QtGui.QLabel(u'Период')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QSpinBox()
		spinBox.setMinimum(0)
		layout.addWidget(spinBox, 0, 1)
		return layout
		
		
class DigitalSignal6(DigitalSignal):
	def getDataFromLayout(self, layout):
		self.L = layout.itemAtPosition(0, 1).widget().value()		
		
	def generate(self):
		u = [(i % L) / (L + 0.0)  for i in range(self.N)]
		return u
		
	def fillLayout(self, layout):
		label = QtGui.QLabel(u'Период')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QSpinBox()
		spinBox.setMinimum(0)
		layout.addWidget(spinBox, 0, 1)
		return layout

class DigitalSignal7(DigitalSignal):
	def generate(self):
		u = [a * math.exp(-i / (self.tau + 0.0)) * math.cos(self.omega * i + self.phi) for i in range(self.N)]
		return u

	def getDataFromLayout(self, layout):
		self.a = layout.itemAtPosition(0, 1).widget().value()	
		self.omega = layout.itemAtPosition(1, 1).widget().value()
		self.phi = layout.itemAtPosition(2, 1).widget().value()		
		self.tau = layout.itemAtPosition(3, 1).widget().value()		
		
	def fillLayout(self, layout):
		label = QtGui.QLabel(u'Амплитуда')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'Частота')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 1, 1)
		label = QtGui.QLabel(u'Начальная фаза')
		layout.addWidget(label, 2, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 2, 1)
		label = QtGui.QLabel(u'Параметр ширины огибающей')
		layout.addWidget(label, 3, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 3, 1)
		return layout				
		
class DigitalSignal8(DigitalSignal):
	def generate(self):
		u = [a * math.cos(self.u * i) * math.cos(self.omega * i + self.phi) for i in range(self.N)]
		return u

	def getDataFromLayout(self, layout):
		self.a = layout.itemAtPosition(0, 1).widget().value()	
		self.omega = layout.itemAtPosition(1, 1).widget().value()
		self.phi = layout.itemAtPosition(2, 1).widget().value()		
		self.u = layout.itemAtPosition(3, 1).widget().value()				
		
	def fillLayout(self, layout):
		label = QtGui.QLabel(u'Амплитуда')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'Частота')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 1, 1)
		label = QtGui.QLabel(u'Начальная фаза')
		layout.addWidget(label, 2, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 2, 1)
		label = QtGui.QLabel(u'Частота огибающей')
		layout.addWidget(label, 3, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 3, 1)
		return layout			
		
class DigitalSignal9(DigitalSignal):
	def generate(self):
		u = [a * (1 + self.m * math.cos(self.u * i)) * math.cos(self.omega * i + self.phi) for i in range(self.N)]
		return u

	def getDataFromLayout(self, layout):
		self.a = layout.itemAtPosition(0, 1).widget().value()	
		self.omega = layout.itemAtPosition(1, 1).widget().value()
		self.phi = layout.itemAtPosition(2, 1).widget().value()		
		self.u = layout.itemAtPosition(3, 1).widget().value()	
		self.m = layout.itemAtPosition(4, 1).widget().value()			
		
	def fillLayout(self, layout):
		label = QtGui.QLabel(u'Амплитуда')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'Частота')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 1, 1)
		label = QtGui.QLabel(u'Начальная фаза')
		layout.addWidget(label, 2, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 2, 1)
		label = QtGui.QLabel(u'Частота огибающей')
		layout.addWidget(label, 3, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 3, 1)
		label = QtGui.QLabel(u'Индекс глубины модуляции')
		layout.addWidget(label, 4, 0)
		spinBox = QtGui.QDoubleSpinBox()
		layout.addWidget(spinBox, 4, 1)
		return layout					
		
class DigitalSignal10(DigitalSignal):
	def generate(self):
		u = [random.randint(self.a, self.b) for i in range(self.N)]
		return u
	
	def getDataFromLayout(self, layout):
		self.a = layout.itemAtPosition(0, 1).widget().value()	
		self.b = layout.itemAtPosition(1, 1).widget().value()	

	def fillLayout(self, layout):
		label = QtGui.QLabel(u'a')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QSpinBox()
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'b')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QSpinBox()
		layout.addWidget(spinBox, 1, 1)
		return layout		
		
class DigitalSignal11(DigitalSignal):
	def generate(self):
		u = [np.random.normal(self.a, self.sigma_2) for i in range(self.N)]
		return u

	def getDataFromLayout(self, layout):
		self.a = layout.itemAtPosition(0, 1).widget().value()	
		self.sigma_2 = layout.itemAtPosition(1, 1).widget().value()	

	def fillLayout(self, layout):
		label = QtGui.QLabel(u'a')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QSpinBox()
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'sigma^2')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QSpinBox()
		layout.addWidget(spinBox, 1, 1)
		return layout				
		
class DigitalSignal12(DigitalSignal):
	def generate(self):
		x = [np.random.normal(0, self.sigma_2) for i in range(self.N)]
		y = []
		for i in range(self.N):
			s1 = 0
			s2 = 0
			for j in range(min(len(self.a), i)):
				s1 += self.a[j] * y[i - j];
			for j in range(min(len(self.b), i)):
				s2 += self.b[j] * x[i - j];
			y.append(x[i] + s2 - s1)
		return y

	def getDataFromLayout(self, layout):
		p = layout.itemAtPosition(0, 0).widget().value()
		a = layout.itemAtPosition(0, 3).widget()
		self.a = [int(a.item(i, 0).widget().text()) for i in range(p)]
		q = layout.itemAtPosition(1, 0).widget().value()
		b = layout.itemAtPosition(1, 3).widget()
		self.a = [int(b.item(i, 0).widget().text()) for i in range(q)]
		self.sigma_2 = layout.itemAtPosition(2, 1).widget().value()	

	def fillLayout(self, layout):
		self.layout = layout
		label = QtGui.QLabel(u'p')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QSpinBox()
		spinBox.setMinimum(0)
		spinBox.valueChanged.connect(self.changed)
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'a')
		layout.addWidget(label, 0, 2)
		spinBox = QtGui.QTableWidget ()
		spinBox.setColumnCount(1)
		spinBox.setRowCount(0)
		layout.addWidget(spinBox, 0, 3)
		label = QtGui.QLabel(u'q')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QSpinBox()
		spinBox.valueChanged.connect(self.changed)
		spinBox.setMinimum(0)
		layout.addWidget(spinBox, 1, 1)
		label = QtGui.QLabel(u'b')
		layout.addWidget(label, 1, 2)
		spinBox = QtGui.QTableWidget ()
		spinBox.setColumnCount(1)
		spinBox.setRowCount(0)
		layout.addWidget(spinBox, 1, 3)
		label = QtGui.QLabel(u'sigma^2')
		layout.addWidget(label, 2, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.setMinimum(0)
		layout.addWidget(spinBox, 2, 1)
		return layout		

	def changed(self):
		self.layout.itemAtPosition(0, 3).widget().setRawCount(self.layout.itemAtPosition(0, 0).widget().value())
		self.layout.itemAtPosition(1, 3).widget().setRawCount(self.layout.itemAtPosition(1, 0).widget().value())

class Lab4(Labs_):
	generatedSignal = QtCore.pyqtSignal()
	analyzedSignal = QtCore.pyqtSignal()

	def __init__(self, parent):
		super(Lab4, self).__init__(parent, 1)
		self.parent = parent

		self.verticalLayout = QtGui.QHBoxLayout(self)
		self.setLayout(self.verticalLayout)
		
		self.sc1 = MyStaticMplCanvas(self, width=1000, height=1000, dpi=100)
		
		tabWidget = QtGui.QTabWidget(self)
		self.verticalLayout.addWidget(tabWidget)
		tabWidget.addTab(self.sc1, u'Сигнал')
		
		layout = QtGui.QVBoxLayout(self)
		self.verticalLayout.addLayout(layout)
		
		self.solLayout = QtGui.QGridLayout(self)
		layout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		layout.addLayout(self.solLayout)
		
		label = QtGui.QLabel(u'Источник выборки')
		self.solLayout.addWidget(label, 0, 0)
		self.source = QtGui.QComboBox(self)
		self.solLayout.addWidget(self.source, 0, 1)
		self.source.addItems([u'Сгенерировать', u'Загрузить из файла'])
		self.source.currentIndexChanged.connect(self.changeControlsVisibility)
		
		self.selectFile = QtGui.QPushButton(self)
		self.selectFile.setText(u'Выбрать файл')
		self.solLayout.addWidget(self.selectFile, 1, 0)
		self.selectFile.clicked.connect(self.selectFilePressed)
		
		label = QtGui.QLabel(u'Количество отсчетов')
		self.solLayout.addWidget(label, 2, 0)
		self.expNum = QtGui.QSpinBox(self)
		self.solLayout.addWidget(self.expNum, 2, 1)
		self.expNum.setRange(1, 1000000000)
		self.expNum.setValue(100)

		label = QtGui.QLabel(u'Не сохранять в файл')
		self.solLayout.addWidget(label, 3, 0)
		self.dontSave = QtGui.QCheckBox(self)
		self.solLayout.addWidget(self.dontSave, 3, 1)
		self.generateBtn = QtGui.QPushButton(self)
		self.generateBtn.setText(u'Сгенерировать сигнал')
		self.generateBtn.clicked.connect(self.generate)
		self.solLayout.addWidget(self.generateBtn, 4, 0)
		self.isGeneratedLabel = QtGui.QLabel(u'Сигнал не сгенерирован')
		self.solLayout.addWidget(self.isGeneratedLabel, 4, 1)
		self.dontSave.setChecked(True)

		self.calc = QtGui.QPushButton(self)
		self.calc.setText(u'Анализировать сигнал')
		self.calc.clicked.connect(self.count)
		self.solLayout.addWidget(self.calc, 5, 0)
		self.generatedSignal.connect(self.generated)
		self.analyzedSignal.connect(self.analyzed)
		
		#self.frstVar = QtGui.QComboBox(self)
		#self.frstVar.currentIndexChanged.connect(self.frstVarChanged)
		#self.solLayout.addWidget(self.frstVar, 6, 0)

		#self.scndVar = QtGui.QComboBox(self)
		#self.scndVar.currentIndexChanged.connect(self.scndVarChanged)
		#self.solLayout.addWidget(self.scndVar, 6, 1)

		self.showResults = QtGui.QPushButton(self)
		self.showResults.setText(u'Показать выборочные данные')
		self.showResults.clicked.connect(self.showStat)
		self.solLayout.addWidget(self.showResults, 6, 0)	
			
		self.isGenerated = False	
		self.parameters = None	
		self.results = None
		self.changeControlsVisibility()

		self.signalsCombobox = QtGui.QComboBox(self)
		self.signalsCombobox.currentIndexChanged.connect(self.signalsComboboxChanged)
		self.solLayout.addWidget(self.signalsCombobox, 7, 0)


		label = QtGui.QLabel(u'graph type')
		self.solLayout.addWidget(label, 8, 0)
		self.graphType = QtGui.QComboBox(self)
		self.graphType.currentIndexChanged.connect(self.graphTypeChanged)
		self.solLayout.addWidget(self.graphType, 8, 1)
		self.graphType.addItem(str(0))
		self.graphType.addItem(str(1))
		
		self.signalLayouts = []
		for i in range(12):
			self.signalsCombobox.addItem(str(i + 1))
			layout = QtGui.QGridLayout(self)
			signal = globals()['DigitalSignal{0}'.format(i + 1)](0)
			layout = signal.fillLayout(layout)
			self.signalLayouts.append(layout)
			self.solLayout.addLayout( layout, 9, 0)
			for j in range(layout.count()):
				layout.itemAt(j).widget().setVisible(False)
		self.hideSignalLayouts(0)
		
	def hideSignalLayouts(self, index):
		for i in range(12):
			layout = self.signalLayouts[i]
			for j in range(layout.count()):
					layout.itemAt(j).widget().setVisible(i == index)
	
	def signalsComboboxChanged(self, index):
		self.hideSignalLayouts(index)

	def draw(self):
		self.sc1.clear()
		if (self.graphType.currentIndex() ==0 ):	
			self.sc1.vlines(range(self.N), [0 for i in range(self.N)], self.u)
		else:
			self.sc1.plot(range(self.N), self.u, '-', 'red')

	def graphTypeChanged(self, index):
		if (self.isGenerated):
			self.draw()

	def showStat(self):
		statDialog = ResultsDialog(self, self.parameters, self.results)
		statDialog.open()

	def selectFilePressed(self):
		fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',  os.getcwd())
		if os.path.isfile(fname):
			self.isGeneratedLabel.setText(u'Загружается выборка...')
			self.sample = []
			try:
				f = open(fname, 'r')
				res = f.read().split()
				M = int(res[0])
				exp = [float(res[i + 1]) for i in range(M)]
				cov = []
				l = M + 1
				for i in range(M):
					cov.append([])
					for j in range(M):
						cov[i].append(float(res[l]))
						l += 1
				parameters = DistributionParameters(1, M, exp, cov)
				N = int(res[l])
				self.expNum.setValue(N)
				l += 1
				for i in range(N):
					self.sample.append([])
					for j in range(M):
						self.sample[i].append(float(res[l]))
						l += 1
				f.close()
				self.isGenerated = True
				self.parametersGot(parameters)
				self.isGeneratedLabel.setText(u'Выборка загружена')			
			except:
				self.isGeneratedLabel.setText(u'Выборка не сгенерирована')
				showMessage(u'Ошибка', u'Некорректный формат файла')

	def generated(self):
		self.isGeneratedLabel.setText(u'Выборка сгенерирована')
		self.isGenerated = True
		self.changeControlsVisibility()
		self.parent.changeState('')

	def analyzed(self):
		if self.analyzeCnt < 2:
			return
		self.sc1.draw_()
		self.changeControlsVisibility()
		self.parent.changeState('')
			
	def startGenerate(self):
		self.changeControlsVisibility()
		self.N = self.expNum.value()
		index = self.signalsCombobox.currentIndex() 
		signal = globals()['DigitalSignal{0}'.format(index + 1)](self.N)
		signal.getDataFromLayout(self.signalLayouts[index])
		self.u = signal.generate()
		self.isGenerated = True
		self.draw()
		#self.sc1.draw_();
		self.generatedSignal.emit()		
		
	def countStatParams(self):
		N = len(self.sample)
		M = self.parameters.dimension
		m = [0 for i in range(M)]
		for i in range(M):
			sum = 0
			for j in range(N):
				sum += self.sample[j][i]
			m[i] = (sum + 0.0) / N

		r = [[0 for i in range(M)] for j in range(M)]
		for j in range(M):
			for l in range(M):
				sum = 0
				for i in range(N):
					sum += (self.sample[i][j] - m[j]) * (self.sample[i][l] - m[l])
				r[j][l] = r[l][j] = (sum + 0.0) / N

		self.results = DistributionParameters(1, M, m, r)

		x_ = self.frstVar.currentIndex()
		y_ = self.scndVar.currentIndex()
		N = 1000
		x1 = np.linspace(-(self.results.covariation[x_][x_] + 7) + self.results.expectations[x_], 
			(self.results.covariation[x_][x_] + 7) + self.results.expectations[x_], N)
		y1 = np.linspace(-(self.results.covariation[y_][y_] + 7) + self.results.expectations[y_], 
			(self.results.covariation[y_][y_] + 7) + self.results.expectations[y_], N)

		X, Y = np.meshgrid(x1, y1)
		Z = mlab.bivariate_normal(X, Y, math.sqrt(self.results.covariation[x_][x_]), 
			math.sqrt(self.results.covariation[y_][y_]), self.results.expectations[x_],
			self.results.expectations[y_], self.results.covariation[x_][y_])
		self.sc1.contour(X, Y, Z, 10, 'yellow')	
		
		self.analyzeCnt += 1
		self.analyzedSignal.emit()	
		
	def startAnalyze(self):
		x_ = self.frstVar.currentIndex()
		y_ = self.scndVar.currentIndex()
		x = []
		y = []
		if self.expNum.value() > 1000000: #10^6 -- maxsize
			for i in range(self.expNum.value()):
				if random.randint(0, self.expNum.value() - 1) < 1000000:
					x.append(self.sample[i][x_])
					y.append(self.sample[i][y_])
		else:
			x = [self.sample[i][x_] for i in range(self.expNum.value())]
			y = [self.sample[i][y_] for i in range(self.expNum.value())]
		self.sc1.clear()
		self.sc1.plot(x, y, '.', 'black')	
		N = 1000
		x1 = np.linspace(-(self.parameters.covariation[x_][x_] + 7) + self.parameters.expectations[x_], 
			(self.parameters.covariation[x_][x_] + 7) + self.parameters.expectations[x_], N)
		y1 = np.linspace(-(self.parameters.covariation[y_][y_]  + 7)+ self.parameters.expectations[y_], 
			(self.parameters.covariation[y_][y_] + 7 ) + self.parameters.expectations[y_], N)

		X, Y = np.meshgrid(x1, y1)
		Z = mlab.bivariate_normal(X, Y, math.sqrt(self.parameters.covariation[x_][x_]), 
			math.sqrt(self.parameters.covariation[y_][y_]), self.parameters.expectations[x_],
			self.parameters.expectations[y_], self.parameters.covariation[x_][y_])
		self.sc1.contour(X, Y, Z, 10, 'red')	

		self.analyzeCnt += 1
		self.analyzedSignal.emit()		
		
	def generate(self):
		self.isGeneratedLabel.setText(u'Выборка не сгенерирована')
		self.results = None
		self.parent.changeState(u'Выполняется...')
		thread = labThread4(self, self.startGenerate)
		thread.start()

	def changeControlsVisibility(self):
		i = self.source.currentIndex()
		self.selectFile.setVisible(i)
		self.calc.setDisabled(self.parameters is None or not self.isGenerated)
		self.showResults.setDisabled(self.results is None or not self.isGenerated)
		
	def count(self):
		self.analyzeCnt = 0;
		self.parent.changeState(u'Анализируется...')
		thread1 = labThread4(self, self.startAnalyze)
		thread1.start()
		thread2 = labThread4(self, self.countStatParams)
		thread2.start()

