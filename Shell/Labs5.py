#-*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import random, math
import os.path
import os
import time
import threading 
from Misc import *
from Labs import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import mlab
import pylab
import numpy as np
import numpy.linalg as linalg
#from scipy import interpolate
from matplotlib import rcParams
import copy
import cmath
#from spectrum import DaniellPeriodogram

class MyMplCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=5, dpi=100):
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
	def plot(self, x, y, ch, col):
		if ch:
			self.axes.plot(x, y, ch, zorder = 0, color = col)
		else:
			self.axes.plot(x, y, zorder = 0, color = col)
		#self.draw()
		
	def contour(self, X, Y, Z, lvlsNum, col):
		CS = self.axes.contour(X, Y, Z, lvlsNum, colors = col)
		#self.axes.clabel(CS, inline=1, fontsize=10)
		#self.draw()
		
	def hist(self, x, b = 28):
		self.axes.hist(x, bins = b, normed = True)
		self.draw()

	def clear(self):
		#self.axes.hold(False)
		self.axes.plot([], [])
		#self.axes.hold(True)
	
	def draw_(self):
		self.draw()

	def set_zorder(self, level):
		self.axes.set_zorder(level)
		
class DistributionParameters():
	def __init__(self, dimension, expectations, covariation, density):
		self.dimension = dimension
		self.expectation = np.array(expectations)
		self.covariation = np.array(covariation)
		self.density = density
			
	def covariationIsValid(self):
		try:
			L = linalg.cholesky(self.covariation)
		except:	
			showMessage('Error', 'Matrix is not positive definite')
			return False
		for i in range(self.dimension):
			for j in range(self.dimension):
				if self.covariation[i][j] != self.covariation[j][i]:
					showMessage('Error', 'Matrix is not symmetric')
					return False

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
		self.initExpectationsVector(self.parameters.expectation, self.expectationVector1, self.parameters.dimension)

		self.expectationVector2 = QtGui.QTableWidget(self)
		self.layout.addWidget(self.expectationVector2, 1, 2)
		self.initExpectationsVector(self.results.expectation, self.expectationVector2, self.results.dimension)

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
	
class DistributionParametersUI():
	def __init__(self, parent, layout, dimension, numberOfClasses, source):
		self.parent = parent
		self.layout = layout
		self.dimension = dimension
		self.expectationVectors = []
		self.covariationMatrixes = []
		self.density = []
		self.expLabels = []
		self.covLabels = []
		self.densityLabels = []
		self.numberOfClasses = numberOfClasses
		self.distribution = []
		print source
		print self.numberOfClasses
		print dimension, numberOfClasses
		for i in range(self.numberOfClasses):
			self.expLabels.append(QtGui.QLabel(u'Вектор средних %s' % (i + 1)))
			self.expLabels[i].setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
			self.expLabels[i].setMaximumSize(QtCore.QSize(150, 30))
			self.layout.addWidget(self.expLabels[i], 3 + 3 * i, 0)
			self.expectationVectors.append(QtGui.QTableWidget(self.parent))
			self.expectationVectors[i].setRowCount(1)
			self.expectationVectors[i].setColumnCount(dimension)
			self.expectationVectors[i].setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
			self.layout.addWidget(self.expectationVectors[i], 3 + 3 *i, 1)

			self.covLabels.append(QtGui.QLabel(u'Матрица ковариации %s' % (i + 1)))
			self.covLabels[i].setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
			self.covLabels[i].setMaximumSize(QtCore.QSize(150, 30))
			self.layout.addWidget(self.covLabels[i], 4 + 3 * i, 0)
			self.covariationMatrixes.append(QtGui.QTableWidget(self.parent))
			self.covariationMatrixes[i].setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
			self.layout.addWidget(self.covariationMatrixes[i], 4 + 3 * i, 1)
			self.covariationMatrixes[i].setRowCount(dimension)
			self.covariationMatrixes[i].setColumnCount(dimension)
			self.distribution.append(DistributionParameters(dimension, [], [], 0))
			expectation = []
			covariation = []
			for j in range(dimension):
				print i, j, source[i].expectation[j] if source else 0
				expectation.append(source[i].expectation[j] if source else 0)
				item = QtGui.QTableWidgetItem(str(expectation[j]))
				self.expectationVectors[i].setItem(0, j, item)	
			
			self.distribution[i].expectation = np.array(expectation)	
			

			for k in range(dimension):
				covariation.append([])
				for j in range(dimension):
					covariation[k].append(source[i].covariation[k][j] if source else 0)
					item = QtGui.QTableWidgetItem(str(covariation[k][j]))
					self.covariationMatrixes[i].setItem(k, j, item)	
			self.distribution[i].covariation = np.array(covariation)
			
			self.densityLabels.append(QtGui.QLabel(u'Априорная вероятность %s' % (i + 1)))
			self.densityLabels[i].setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
			self.densityLabels[i].setMaximumSize(QtCore.QSize(150, 30))
			self.layout.addWidget(self.densityLabels[i], 5 + 3 * i, 0)
			self.density.append(QtGui.QDoubleSpinBox(self.parent))
			self.density[i].setMinimum(0)
			self.density[i].setMaximum(1)
			density = source[i].density if source else 0
			self.density[i].setValue(density)
			self.density[i].setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
			self.layout.addWidget(self.density[i], 5 + 3 *i, 1)	
			
	def changeNumberOfClasses(self, numberOfClasses):
		for i in range(numberOfClasses, len(self.expectationVectors)):
			self.expectationVectors[i].setVisible(False)
			self.expLabels[i].setVisible(False)
			self.covariationMatrixes[i].setVisible(False)
			self.covLabels[i].setVisible(False)
			self.density[i].setVisible(False)
			self.densityLabels[i].setVisible(False)
			
			
		for i in range(self.numberOfClasses, min(len(self.expectationVectors), numberOfClasses)):
			self.expectationVectors[i].setVisible(True)
			self.expLabels[i].setVisible(True)		
			self.covariationMatrixes[i].setVisible(True)
			self.covLabels[i].setVisible(True)
			self.density[i].setVisible(True)
			self.densityLabels[i].setVisible(True)
			
		for i in range(len(self.expectationVectors), numberOfClasses):
			self.expLabels.append(QtGui.QLabel(u'Вектор средних %s' % (i + 1)))
			self.expLabels[i].setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
			self.expLabels[i].setMaximumSize(QtCore.QSize(150, 30))
			self.layout.addWidget(self.expLabels[i], 3 + 3 * i, 0)
			self.expectationVectors.append(QtGui.QTableWidget(self.parent))
			self.expectationVectors[i].setRowCount(1)
			self.expectationVectors[i].setColumnCount(self.dimension)
			self.expectationVectors[i].setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
			self.layout.addWidget(self.expectationVectors[i], 3 + 3 * i, 1)
			self.covLabels.append(QtGui.QLabel(u'Матрица ковариации %s' % (i + 1)))
			self.covLabels[i].setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
			self.covLabels[i].setMaximumSize(QtCore.QSize(150, 30))
			self.layout.addWidget(self.covLabels[i], 4 +  3 * i, 0)
			self.covariationMatrixes.append(QtGui.QTableWidget(self.parent))
			self.covariationMatrixes[i].setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
			self.covariationMatrixes[i].setRowCount(self.dimension)
			self.covariationMatrixes[i].setColumnCount(self.dimension)
			self.layout.addWidget(self.covariationMatrixes[i], 4 + 3* i, 1)
			for j in range(self.dimension):
				item = QtGui.QTableWidgetItem(str(0))
				self.expectationVectors[i].setItem(0, j, item)	
			for k in range(self.dimension):
				for j in range(self.dimension):
					item = QtGui.QTableWidgetItem(str(0))
					self.covariationMatrixes[i].setItem(k, j, item)	
			self.densityLabels.append(QtGui.QLabel(u'Априорная вероятность %s' % (i + 1)))
			self.densityLabels[i].setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
			self.densityLabels[i].setMaximumSize(QtCore.QSize(150, 30))
			self.layout.addWidget(self.densityLabels[i], 5 + 3 * i, 0)
			self.density.append(QtGui.QDoubleSpinBox(self.parent))
			self.density[i].setMinimum(0)
			self.density[i].setMaximum(1)
			self.density[i].setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
			self.layout.addWidget(self.density[i], 5 + 3 *i, 1)	

			self.distribution.append(DistributionParameters(self.dimension, 
				[0 for i in range(self.dimension)], 
				[[0 for i in range(self.dimension)] for j in range(self.dimension)], 0))
			
		self.numberOfClasses = numberOfClasses
		
	def changeDimension(self, dimension):		
		self.dimension = dimension	
		for i in range(len(self.expectationVectors)):
			self.expectationVectors[i].setColumnCount(self.dimension)
			
			self.covariationMatrixes[i].setRowCount(self.dimension)
			self.covariationMatrixes[i].setColumnCount(self.dimension)
			
			for k in range(self.dimension):
				item = self.expectationVectors[i].item(0, k)
				if not item:
					item = QtGui.QTableWidgetItem('0')
					self.expectationVectors[i].setItem(0, k, item)
				elif item.text() == '':
					item.setText('0')
				for j in range(self.dimension):
					item = self.covariationMatrixes[i].item(k, j)
					if not item:
						item = QtGui.QTableWidgetItem('0' if k != j else '1')
						self.covariationMatrixes[i].setItem(k, j, item)
					elif item.text() == '':
						item.setText('0' if k != j else '1')	
			
	def getDistributionParameters(self):	
		self.distribution = []
		for i in range(self.numberOfClasses):
			self.distribution.append(DistributionParameters(self.dimension, 
				[float(self.expectationVectors[i].item(0, j).text()) for j in range(self.dimension)], 
				[[float(self.covariationMatrixes[i].item(k, j).text()) for j in range(self.dimension)] for k in range(self.dimension)], 
				self.density[i].value()))
		return self.distribution;

	def covariationIsValid(self):
		result = True
		for k in range(self.numberOfClasses):
			result = result and self.distribution[k].covariationIsValid();
		return result

	def densityIsValid(self):
		result = 0
		for k in range(self.numberOfClasses):
			result += self.distribution[k].density
		if result != 1:
			showMessage('Error', 'Densities sum mest be 1')
		return result == 1
		
class ParametersDialog(QtGui.QDialog):
	def __init__(self, parent, initParams = None):
		super(ParametersDialog, self).__init__(parent)
		
		self.parent = parent
		
		self.layout = QtGui.QGridLayout(self)
		self.layout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
		self.setLayout(self.layout)
		
		label = QtGui.QLabel(u'Количество классов')
		label.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		label.setMaximumSize(QtCore.QSize(150, 30))
		self.layout.addWidget(label, 0, 0)
		self.classesNumber = QtGui.QSpinBox(self)
		self.classesNumber.setMinimum(2)
		self.classesNumber.setValue(len(initParams) if initParams else 2)
		self.classesNumber.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.layout.addWidget(self.classesNumber, 0, 1)
		self.classesNumber.valueChanged.connect(self.classesNumberChanged)
		
		label = QtGui.QLabel(u'Размерность выборки')
		label.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
		label.setMaximumSize(QtCore.QSize(150, 30))
		self.layout.addWidget(label, 1, 0)
		self.distributionDimension = QtGui.QSpinBox(self)
		self.distributionDimension.setMinimum(2)
		self.distributionDimension.setValue(initParams[0].dimension if initParams else 2)
		self.distributionDimension.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		self.layout.addWidget(self.distributionDimension, 1, 1)
		self.distributionDimension.valueChanged.connect(self.dimensionChanged)
		
		bb = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok or QDialogButtonBox.Cancel)
		self.layout.addWidget(bb, 2, 0)
		bb.accepted.connect(self.onAccept)

		self.distributionParameters= DistributionParametersUI(self, self.layout, self.distributionDimension.value(), self.classesNumber.value(), initParams);
			
	def onAccept(self):
		dp = self.distributionParameters.getDistributionParameters()
		result = self.distributionParameters.covariationIsValid() and self.distributionParameters.densityIsValid()
		if result:
			self.parent.parametersGot(dp)
			self.parent.results = None
			self.close();
		
	def dimensionChanged(self):
		self.distributionParameters.changeDimension(self.distributionDimension.value())	

	def classesNumberChanged(self):
		self.distributionParameters.changeNumberOfClasses(self.classesNumber.value())	
	
class Lab5(Labs_):
	generatedSignal = QtCore.pyqtSignal()
	analyzedSignal = QtCore.pyqtSignal()

	def __init__(self, parent):
		super(Lab5, self).__init__(parent, 1)
		self.parent = parent

		self.verticalLayout = QtGui.QHBoxLayout(self)
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
		self.dontSave.setChecked(True)

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
		paramsDialog = ParametersDialog(self, self.parameters)
		paramsDialog.open()
	
	def parametersGot(self, parameters):
		self.parameters = parameters
		self.frstVar.clear()
		self.scndVar.clear()
		for i in range (self.parameters[0].dimension):
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
		N = self.expNum.value()
		self.isGenerated = False
		self.changeControlsVisibility()
		for i in range(len(self.parameters)):
			self.sample = np.random.multivariate_normal(self.parameters[i].expectation, 
					self.parameters[i].covariation, N)
		if not self.dontSave.isChecked():
			f = open('result.txt', 'w')
			f.write('%s %s\n' %  (self.expNum.value(), self.parameters.dimension))
			for i in range(self.expNum.value()):
				for j in range(self.parameters.dimension):
					f.write('%s ' %  self.sample[i][j])
				f.write('\n');
			f.close()
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
			for l in range(j, M):
				sum = 0
				for i in range(N):
					sum += (self.sample[i][j] - m[j]) * (self.sample[i][l] - m[l])
				r[j][l] = r[l][j] = (sum + 0.0) / N

		self.results = DistributionParameters(1, M, m, r)

		x_ = self.frstVar.currentIndex()
		y_ = self.scndVar.currentIndex()
		N = 100
		x1 = np.linspace(-(self.results.covariation[x_][x_] + 7) + self.results.expectation[x_], 
			(self.results.covariation[x_][x_] + 7) + self.results.expectation[x_], N)
		y1 = np.linspace(-(self.results.covariation[y_][y_] + 7) + self.results.expectation[y_], 
			(self.results.covariation[y_][y_] + 7) + self.results.expectation[y_], N)

		X, Y = np.meshgrid(x1, y1)
		Z = mlab.bivariate_normal(X, Y, math.sqrt(self.results.covariation[x_][x_]), 
			math.sqrt(self.results.covariation[y_][y_]), self.results.expectation[x_],
			self.results.expectation[y_], self.results.covariation[x_][y_])
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
		N = 100
		x1 = np.linspace(-(self.parameters.covariation[x_][x_] + 7) + self.parameters.expectation[x_], 
			(self.parameters.covariation[x_][x_] + 7) + self.parameters.expectation[x_], N)
		y1 = np.linspace(-(self.parameters.covariation[y_][y_]  + 7)+ self.parameters.expectation[y_], 
			(self.parameters.covariation[y_][y_] + 7 ) + self.parameters.expectation[y_], N)

		X, Y = np.meshgrid(x1, y1)
		Z = mlab.bivariate_normal(X, Y, math.sqrt(self.parameters.covariation[x_][x_]), 
			math.sqrt(self.parameters.covariation[y_][y_]), self.parameters.expectation[x_],
			self.parameters.expectation[y_], self.parameters.covariation[x_][y_])
		self.sc1.contour(X, Y, Z, 10, 'red')	

		self.analyzeCnt += 1
		self.analyzedSignal.emit()		
		
	def generate(self):
		self.isGeneratedLabel.setText(u'Выборка не сгенерирована')
		self.results = None
		self.sample = []
		self.parent.changeState(u'Выполняется...')
		thread = threading.Thread(target=self.startGenerate)
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
		self.analyzeCnt = 0;
		self.parent.changeState(u'Анализируется...')
		thread1 = threading.Thread(target=self.startAnalyze)
		thread1.start()
		thread2 = threading.Thread(target=self.countStatParams)
		thread2.start()

