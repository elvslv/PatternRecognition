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

class MyMplCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(111)
# We want the axes cleared every time plot() is called
		#self.axes.hold(False)
		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
		                           QtGui.QSizePolicy.Expanding,
		                           QtGui.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

class MyStaticMplCanvas(MyMplCanvas):
	def plot(self, x, y, ch):
		if ch:
			self.axes.plot(x, y, ch, zorder = 0)
		else:
			self.axes.plot(x, y, zorder = 0)
		#self.draw()
		
	def contour(self, X, Y, Z, lvlsNum):
		CS = self.axes.contour(X, Y, Z, lvlsNum)
		self.axes.clabel(CS, inline=1, fontsize=10)
		#self.draw()
		
	def hist(self, x, b = 28):
		self.axes.hist(x, bins = b, normed = True)
		self.draw()

	def clear(self):
		self.axes.hold(False)
		self.axes.plot([], [])
		self.axes.hold(True)
	
	def draw_(self):
		self.draw()

	def set_zorder(self, level):
		self.axes.set_zorder(level)
		
class labThread3(Thread):
	def __init__ (self, parent, run):
		Thread.__init__(self)
		self.parent = parent
		self.run = run

class DistributionParameters():
	def __init__(self, t, dimension, expectations, covariation):
		if not t:
			self.dimension = dimension.value()
			self.expectations = np.array([float(expectations.item(0, i).text()) for i in range(self.dimension)])
			self.covariation = np.array([[float(covariation.item(i, j).text()) for j in range(self.dimension)] for i in range(self.dimension)])
		else:
			self.dimension = dimension
			self.expectations = np.array(expectations)
			self.covariation = np.array(covariation)
			
		if not self.covariationIsValid():
			return
			
	def covariationIsValid(self):
		return True

class ResultsDialog(QtGui.QDialog):
	def __init__(self, parent, parameters, results):
		super(ResultsDialog, self).__init__(parent)
		
		self.parent = parent
		self.parameters = parameters
		self.results = results
		
		self.layout = QtGui.QGridLayout(self)
		self.layout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		self.setLayout(self.layout)

		label = QtGui.QLabel(u'Теоретические данные')
		self.layout.addWidget(label, 0, 1)
		label = QtGui.QLabel(u'Выборочные данные')
		self.layout.addWidget(label, 0, 2)
		
		label = QtGui.QLabel(u'Вектор средних')
		self.layout.addWidget(label, 1, 0)
		self.expectationVector1 = QtGui.QTableWidget(self)
		self.layout.addWidget(self.expectationVector1, 1, 1)
		self.initExpectationsVector(self.parameters.expectations, self.expectationVector1, self.parameters.dimension)

		self.expectationVector2 = QtGui.QTableWidget(self)
		self.layout.addWidget(self.expectationVector2, 1, 2)
		self.initExpectationsVector(self.results.expectations, self.expectationVector2, self.results.dimension)

		label = QtGui.QLabel(u'Матрица ковариации')
		self.layout.addWidget(label, 2, 0)
		self.covariationMatrix1 = QtGui.QTableWidget(self)
		self.layout.addWidget(self.covariationMatrix1, 2, 1)
		self.initCovariationMatrix(self.parameters.covariation, self.covariationMatrix1, self.parameters.dimension)

		self.covariationMatrix2 = QtGui.QTableWidget(self)
		self.layout.addWidget(self.covariationMatrix2, 2, 2)
		self.initCovariationMatrix(self.results.covariation, self.covariationMatrix2, self.results.dimension)

	def initExpectationsVector(self, source, dest, dimension):
		dest.setColumnCount(dimension)
		dest.setRowCount(1)
		for i in range(dimension):
			item = QtGui.QTableWidgetItem(str(source[i]))
			dest.setItem(0, i, item)

	def initCovariationMatrix(self, source, dest, dimension):
		dest.setRowCount(dimension)
		dest.setColumnCount(dimension)
		for i in range(dimension):
			for j in range(dimension):
				item = QtGui.QTableWidgetItem(str(source[i][j]))
				dest.setItem(i, j, item)
		
		
class ParametersDialog(QtGui.QDialog):
	def __init__(self, parent):
		super(ParametersDialog, self).__init__(parent)
		
		self.parent = parent
		
		self.layout = QtGui.QGridLayout(self)
		self.layout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		self.setLayout(self.layout)
		
		label = QtGui.QLabel(u'Размерность выборки')
		self.layout.addWidget(label, 0, 0)
		self.distributionDimension = QtGui.QSpinBox(self)
		self.distributionDimension.setMinimum(2)
		self.layout.addWidget(self.distributionDimension, 0, 1)
		self.distributionDimension.valueChanged.connect(self.dimensionChanged)
		
		label = QtGui.QLabel(u'Вектор средних')
		self.layout.addWidget(label, 1, 0)
		self.expectationVector = QtGui.QTableWidget(self)
		self.expectationVector.setRowCount(1)
		self.layout.addWidget(self.expectationVector, 1, 1)

		label = QtGui.QLabel(u'Матрица ковариации')
		self.layout.addWidget(label, 2, 0)
		self.covariationMatrix = QtGui.QTableWidget(self)
		self.layout.addWidget(self.covariationMatrix, 2, 1)
		
		bb = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok or QDialogButtonBox.Cancel)
		self.layout.addWidget(bb, 3, 0)
		bb.accepted.connect(self.onAccept)
		self.dimensionChanged()

	def onAccept(self):
		dp = DistributionParameters(0, self.distributionDimension, self.expectationVector, self.covariationMatrix)
		if (dp):
			self.parent.parametersGot(dp)
			self.parent.results = None
			self.close();
		else:
			showMessage(u'Неправильные параметры')
		
	def dimensionChanged(self):
		self.expectationVector.setColumnCount(self.distributionDimension.value())
		
		self.covariationMatrix.setColumnCount(self.distributionDimension.value())
		self.covariationMatrix.setRowCount(self.distributionDimension.value())
		
		for i in range(self.distributionDimension.value()):
			item = self.expectationVector.item(0, i)
			if not item:
				item = QtGui.QTableWidgetItem('0')
				self.expectationVector.setItem(0, i, item)
			elif item.text() == '':
				item.setText('0')
			for j in range(self.distributionDimension.value()):
				item = self.covariationMatrix.item(i, j)
				if not item:
					item = QtGui.QTableWidgetItem('0' if i != j else '1')
					self.covariationMatrix.setItem(i, j, item)
				elif item.text() == '':
					item.setText('0' if i != j else '1')			
		
class Lab3(Labs_):
	generatedSignal = QtCore.pyqtSignal()
	analyzedSignal = QtCore.pyqtSignal()

	def __init__(self, parent):
		super(Lab3, self).__init__(parent, 1)
		self.parent = parent

		self.verticalLayout = QtGui.QVBoxLayout(self)
		self.setLayout(self.verticalLayout)
		
		self.sc1 = MyStaticMplCanvas(self, width=1000, height=1000, dpi=100)
		
		tabWidget = QtGui.QTabWidget(self)
		self.verticalLayout.addWidget(tabWidget)
		tabWidget.addTab(self.sc1, u'Плотность распределения')
		
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
		self.expNum.setValue(100000)
		
		self.gen = [[label, self.expNum]]
		
		label = QtGui.QLabel(u'Не сохранять в файл')
		self.solLayout.addWidget(label, 3, 0)
		self.dontSave = QtGui.QCheckBox(self)
		self.solLayout.addWidget(self.dontSave, 3, 1)
		self.generateBtn = QtGui.QPushButton(self)
		self.generateBtn.setText(u'Сгенерировать выборку')
		self.generateBtn.clicked.connect(self.generate)
		self.solLayout.addWidget(self.generateBtn, 4, 0)
		self.isGeneratedLabel = QtGui.QLabel(u'Выборка не сгенерирована')
		self.solLayout.addWidget(self.isGeneratedLabel, 4, 1)
		self.gen[0].extend([label, self.dontSave, self.generateBtn, self.isGeneratedLabel])	

		self.calc = QtGui.QPushButton(self)
		self.calc.setText(u'Анализировать выборку')
		self.calc.clicked.connect(self.count)
		self.solLayout.addWidget(self.calc, 5, 0)
		self.generatedSignal.connect(self.generated)
		self.analyzedSignal.connect(self.analyzed)
		
		self.setParametersBtn = QtGui.QPushButton(self)
		self.setParametersBtn.setText(u'Указать параметры выборки')
		self.setParametersBtn.clicked.connect(self.showParametersDialog)
		self.solLayout.addWidget(self.setParametersBtn, 5, 1)

		self.frstVar = QtGui.QComboBox(self)
		self.frstVar.currentIndexChanged.connect(self.frstVarChanged)
		self.solLayout.addWidget(self.frstVar, 6, 0)

		self.scndVar = QtGui.QComboBox(self)
		self.scndVar.currentIndexChanged.connect(self.scndVarChanged)
		self.solLayout.addWidget(self.scndVar, 6, 1)

		self.showResults = QtGui.QPushButton(self)
		self.showResults.setText(u'Показать выборочные данные')
		self.showResults.clicked.connect(self.showStat)
		self.solLayout.addWidget(self.showResults, 7, 0)
			
		self.isGenerated = False	
		self.parameters = None	
		self.results = None
		self.changeControlsVisibility()

	def showStat(self):
		statDialog = ResultsDialog(self, self.parameters, self.results)
		statDialog.open()

	def varIndexChanged(self, var, index):
		if self.frstVar.currentIndex() == self.scndVar.currentIndex():
			tmpVar = self.frstVar if var else self.scndVar
			tmpVar.setCurrentIndex(0 if tmpVar.currentIndex() else 1)
				
	def frstVarChanged(self, index):
		self.varIndexChanged(0, index)

	def scndVarChanged(self, index):
		self.varIndexChanged(1, index)

	def showParametersDialog(self):
		paramsDialog = ParametersDialog(self)
		paramsDialog.open()
	
	def parametersGot(self, parameters):
		self.parameters = parameters
		self.frstVar.clear()
		self.scndVar.clear()
		for i in range (self.parameters.dimension):
			self.frstVar.addItem(str(i + 1))
			self.scndVar.addItem(str(i + 1))
		self.frstVar.setCurrentIndex(0)
		self.scndVar.setCurrentIndex(1)
		self.changeControlsVisibility()
		
	def selectFilePressed(self):
		fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',  os.getcwd())
		if os.path.isfile(fname):
			self.isGeneratedLabel.setText(u'Загружается выборка...')
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
		self.isGeneratedLabel.setText(u'Выборка сгенерирована')
		self.isGenerated = True
		self.changeControlsVisibility()
		self.parent.changeState('')
		#if not self.dontSave.isChecked():
		#	f = open('result.txt', 'w')
		#	f.write('%s ' %  self.expNum.value())
		#	for v in self.sample:
		#		f.write('%s ' %  v)
		#	f.close()

	def analyzed(self):
		self.changeControlsVisibility()
		self.parent.changeState('')
			
	def startGenerate(self):
		N = self.expNum.value()
		self.isGenerated = False
		self.changeControlsVisibility()
		self.sample = np.random.multivariate_normal(self.parameters.expectations, 
				self.parameters.covariation, N)
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
		self.changeControlsVisibility()

		
	def startAnalyze(self):
		x_ = self.frstVar.currentIndex()
		y_ = self.scndVar.currentIndex()
		x = [self.sample[i][x_] for i in range(self.expNum.value())]
		y = [self.sample[i][y_] for i in range(self.expNum.value())]
		self.sc1.clear()
		self.sc1.plot(x, y, '.')	
		N = 1000
		x1 = np.linspace(-5.0, 5.0, N)
		y1 = np.linspace(-5.0, 5.0, N)

		X, Y = np.meshgrid(x1, y1)
		Z = mlab.bivariate_normal(X, Y, self.parameters.covariation[x_][x_], 
			self.parameters.covariation[y_][y_], self.parameters.expectations[x_],
			self.parameters.expectations[y_], self.parameters.covariation[x_][y_])
		self.sc1.contour(X, Y, Z, 10)	
		self.sc1.draw_()
		self.analyzedSignal.emit()		
		
	def generate(self):
		self.isGeneratedLabel.setText(u'Выборка не сгенерирована')
		self.results = None
		self.sample = []
		self.parent.changeState(u'Выполняется...')
		thread = labThread3(self, self.startGenerate)
		thread.start()

	def changeControlsVisibility(self):
		i = self.source.currentIndex()
		for item in self.gen[0]:
			item.setVisible(not i)
		self.selectFile.setVisible(i)
		self.generateBtn.setDisabled(self.parameters is None)
		self.calc.setDisabled(self.parameters is None or not self.isGenerated)
		self.showResults.setDisabled(self.results is None or not self.isGenerated)
		
	def count(self):
		self.parent.changeState(u'Анализируется...')
		thread1 = labThread3(self, self.startAnalyze)
		thread1.start()
		thread2 = labThread3(self, self.countStatParams)
		thread2.start()

