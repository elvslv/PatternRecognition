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
from matplotlib import rcParams
rcParams['text.usetex']=False
rcParams['font.sans-serif'] = ['Times New Roman']
rcParams['font.serif'] = ['Times New Roman'] 

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
		self.axes.hold(False)
		self.axes.margins(1, 1)
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
		self.axes.relim()
		self.axes.margins(0.1, 0)
		self.draw()
		
	def clear(self):
		#self.axes.hold(False)
		self.axes.cla()
		#self.axes.hold(True)
		self.draw()
		self.axes.margins(0.1, 0)
		#self.axes.autoscale(enable=True, axis='both', tight=True)

	def draw_(self):
		self.draw()

	def vlines(self, x, ymin, ymax):
		print x, len(ymin), len(ymax)
		self.axes.vlines(x, ymin, ymax, colors = 'blue')
		self.axes.relim()
		self.draw()
		self.axes.margins(0.1, 0)
		#self.axes.autoscale(enable=True, axis='both', tight=True)
global signal12
signal12 = None

class DigitalSignal:
	def __init__(self, N, parent):
		self.N = N
		self.parent = parent

	def changed2(self):
		pass
		#print self.layout.itemAtPosition(0, 0).widget().value()
		#self.layout.itemAtPosition(0, 3).widget().setRawCount(self.layout.itemAtPosition(0, 0).widget().value())
		#self.layout.itemAtPosition(1, 3).widget().setRawCount(self.layout.itemAtPosition(1, 0).widget().value())
		#self.parent.changed()

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
		spinBox.valueChanged.connect(self.parent.changed)
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
		spinBox.valueChanged.connect(self.parent.changed)
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
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(0.0000000001, 0.9999999999)
		layout.addWidget(spinBox, 0, 1)
		return layout		
		
class DigitalSignal4(DigitalSignal):
	def getDataFromLayout(self, layout):
		self.a = layout.itemAtPosition(0, 1).widget().value()	
		self.omega = layout.itemAtPosition(1, 1).widget().value()
		self.phi = layout.itemAtPosition(2, 1).widget().value()		
		
	def generate(self):
		u = [self.a * math.sin(i * self.omega + self.phi) for i in range(self.N)]
		return u

	def fillLayout(self, layout):
		label = QtGui.QLabel(u'Амплитуда')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'Частота')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		layout.addWidget(spinBox, 1, 1)
		label = QtGui.QLabel(u'Начальная фаза')
		layout.addWidget(label, 2, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		layout.addWidget(spinBox, 2, 1)
		return layout				
		
class DigitalSignal5(DigitalSignal):
	def getDataFromLayout(self, layout):
		self.L = layout.itemAtPosition(0, 1).widget().value()		
	
	def generate(self):
		u = [1 if i % self.L < self.L / 2.0 else -1  for i in range(self.N)]
		return u

	def fillLayout(self, layout):
		label = QtGui.QLabel(u'Период')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setRange(1, 10000000)
		layout.addWidget(spinBox, 0, 1)
		return layout
		
		
class DigitalSignal6(DigitalSignal):
	def getDataFromLayout(self, layout):
		self.L = layout.itemAtPosition(0, 1).widget().value()		
		
	def generate(self):
		u = [(i % self.L) / (self.L + 0.0)  for i in range(self.N)]
		return u
		
	def fillLayout(self, layout):
		label = QtGui.QLabel(u'Период')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setRange(2, 10000000)
		layout.addWidget(spinBox, 0, 1)
		return layout

class DigitalSignal7(DigitalSignal):
	def generate(self):
		u = [self.a * math.exp(-i / (self.tau + 0.0)) * math.cos(self.omega * i + self.phi) for i in range(self.N)]
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
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		spinBox.setValue(0.0000000001)
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'Частота')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		layout.addWidget(spinBox, 1, 1)
		label = QtGui.QLabel(u'Начальная фаза')
		layout.addWidget(label, 2, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		layout.addWidget(spinBox, 2, 1)
		label = QtGui.QLabel(u'Параметр ширины огибающей')
		layout.addWidget(label, 3, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(0.0000000001, 100)
		layout.addWidget(spinBox, 3, 1)
		return layout				
		
class DigitalSignal8(DigitalSignal):
	def generate(self):
		u = [self.a * math.cos(self.u * i) * math.cos(self.omega * i + self.phi) for i in range(self.N)]
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
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		spinBox.setValue(0.0000000001)		
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'Частота')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		spinBox.setValue(0.0000000001)
		layout.addWidget(spinBox, 1, 1)
		label = QtGui.QLabel(u'Начальная фаза')
		layout.addWidget(label, 2, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		spinBox.setValue(0.0000000001)
		layout.addWidget(spinBox, 2, 1)
		label = QtGui.QLabel(u'Частота огибающей')
		layout.addWidget(label, 3, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		spinBox.setValue(0.0000000001)
		layout.addWidget(spinBox, 3, 1)
		return layout			
		
class DigitalSignal9(DigitalSignal):
	def generate(self):
		u = [self.a * (1 + self.m * math.cos(self.u * i)) * math.cos(self.omega * i + self.phi) for i in range(self.N)]
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
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		spinBox.setValue(0.0000000001)
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'Частота')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		spinBox.setValue(0.0000000001)
		layout.addWidget(spinBox, 1, 1)
		label = QtGui.QLabel(u'Начальная фаза')
		layout.addWidget(label, 2, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		spinBox.setValue(0.0000000001)
		layout.addWidget(spinBox, 2, 1)
		label = QtGui.QLabel(u'Частота огибающей')
		layout.addWidget(label, 3, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		spinBox.setValue(0.0000000001)
		layout.addWidget(spinBox, 3, 1)
		label = QtGui.QLabel(u'Индекс глубины модуляции')
		layout.addWidget(label, 4, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setDecimals(10)
		spinBox.setSingleStep(0.0000000001)
		spinBox.setRange(-100, 100)
		spinBox.setValue(0.0000000001)
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
		spinBox.valueChanged.connect(self.parent.changed)
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'b')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
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
		label = QtGui.QLabel(u'Среднее')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'Среднеквадратичное отклонение')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setValue(1)
		layout.addWidget(spinBox, 1, 1)
		return layout				

def signal12Changed(i):
	if not signal12:
		return
	p = signal12.layout.itemAtPosition(0, 1).widget().value()
	q = signal12.layout.itemAtPosition(1, 1).widget().value()
	a = signal12.layout.itemAtPosition(0, 3).widget()
	b = signal12.layout.itemAtPosition(1, 3).widget()
	p1 = a.rowCount()
	q1 = b.rowCount()
	a.setRowCount(p)
	b.setRowCount(q)
	for i in range(p1, p):
		item = QtGui.QTableWidgetItem('0.00')
		a.setItem(i, 0, item)
	for i in range(q1, q):
		item = QtGui.QTableWidgetItem('0.00')
		b.setItem(i, 0, item)		
	signal12.parent.changed()

class DigitalSignal12(DigitalSignal):
	def generate(self):
		x = [np.random.normal(0, self.sigma_2) for i in range(self.N)]
		y = [x[0]]
		for n in range(1, self.N):
			s1 = 0
			s2 = 0
			for i in range(1, min(self.p, n)+1):
				s1 += self.a[i-1] * y[n - i];
			for i in range(1, min(self.q, n)+1):
				s2 += self.b[i-1] * x[n - i];
			y.append(x[n] + s2 - s1)
		return y

	def getDataFromLayout(self, layout):
		p = layout.itemAtPosition(0, 1).widget().value()
		self.p = p
		a = layout.itemAtPosition(0, 3).widget()
		self.a = [float(a.item(i, 0).text()) for i in range(p)]
		q = layout.itemAtPosition(1, 1).widget().value()
		self.q = q
		b = layout.itemAtPosition(1, 3).widget()
		self.b = [float(b.item(i, 0).text()) for i in range(q)]
		self.sigma_2 = layout.itemAtPosition(2, 1).widget().value()	

	def fillLayout(self, layout):
		self.layout = layout
		label = QtGui.QLabel(u'p')
		layout.addWidget(label, 0, 0)
		spinBox = QtGui.QSpinBox()
		spinBox.setMinimum(0)
		spinBox.valueChanged.connect(signal12Changed)
		layout.addWidget(spinBox, 0, 1)
		label = QtGui.QLabel(u'a')
		layout.addWidget(label, 0, 2)
		spinBox = QtGui.QTableWidget()
		spinBox.itemChanged.connect(self.parent.changed)
		spinBox.setColumnCount(1)
		spinBox.setRowCount(0)
		layout.addWidget(spinBox, 0, 3)
		label = QtGui.QLabel(u'q')
		layout.addWidget(label, 1, 0)
		spinBox = QtGui.QSpinBox()
		spinBox.valueChanged.connect(signal12Changed)
		spinBox.setMinimum(0)
		layout.addWidget(spinBox, 1, 1)
		label = QtGui.QLabel(u'b')
		layout.addWidget(label, 1, 2)
		spinBox = QtGui.QTableWidget ()
		spinBox.itemChanged.connect(self.parent.changed)
		spinBox.setColumnCount(1)
		spinBox.setRowCount(0)
		layout.addWidget(spinBox, 1, 3)
		label = QtGui.QLabel(u'Дисперсия')
		layout.addWidget(label, 2, 0)
		spinBox = QtGui.QDoubleSpinBox()
		spinBox.valueChanged.connect(self.parent.changed)
		spinBox.setMinimum(0)
		spinBox.setValue(1)
		layout.addWidget(spinBox, 2, 1)
		return layout		

def DFT(x):
	N = len(x)
	X = []
	for k in range(N):
		X.append(0)
		for n in range(N):
			X[k] += x[n] * (np.cos(-2 * math.pi / N * k * n) + np.sin(-2 * math.pi / N * k * n) * 1j)
	return X

def IDFT(X):
	N = len(X)
	x = []
	for n in range(N):
		x.append(0)
		for k in range(N):
			x[n] += X[k] * (np.cos(2 * math.pi / N * k * n) + np.sin(2 * math.pi / N * k * n) * 1j)
		x[n] = x[n] / N
	return x

def TotalDFT(x, ind):
	return DFT(x) if x == 0 else IDFT(x)

def FFT(x):
	return np.fft.fft(x)

def x_corr(x, ind):
	N = len(x)
	K = []
	sum = 0
	
	for i in range(N):
		sum += x[i]
	sum /= (N + 0.0)
	
	if ind == 0:
		for m in range(N):
			K.append(0)
			for n in range(N - m):
				K[m] += (x[n] - sum) * (x[n + m] - sum)
			K[m] /= (N + 0.0)
	else:
		L = math.pow(2, math.ceil(math.log(2 * N, 2)))
		for i in range(N, L):
			x.append(sum)
		P = FFT(x)
		for m in range(N):
			K.append(0)
			for k in range(L):
				K[m] += P[k] * (np.sin(2 * math.pi / L * m * k) * 1j)
	return K

def x_SPM(x, L):
	P1 = FFT(x)
	P = []
	for k in range(L + 1):
		P.append(0)
		for l in range(-L, L + 1):
			P[k] += P1[k + l]
		P[k] /= (2 * L + 1.0)
	return P
	
def xy_corr(x, y, ind):
	K = []
	sum1 = 0
	sum2 = 0
	N1 = len(x)
	N2 = len(y)
	for i in range(N1):
		sum1 += x[i]
	sum1 /= N1
	for i in range(N2):
		sum2 += y[i]
	sum2 /= N2
	N = max(N1, N2)
	if ind == 0:
		for i in range(N1, N):
			x.append(sum1)
		for i in range(N2, N):
			y.append(sum2)
		for m in range(N):
			K.append(0)
			for n in range(N - m - 1):
				K[m] += (x[n] - sum1) * (y(n + m) - sum2)
			K[m] /= (N + 0.0)
	else:
		for i in range(N1):
			x[i] -= sum1
		for i in range(N2):
			y[i] -= sum2
		N = math.pow(2, math.ceil(math.log(2 * N, 2)))
		for i in range(N1, N):
			x.append(0)
		for i in range(N2, N):
			y.append(0)
		X = FFT(x)
		Y = FFT(y)
		Z = []
		for i in range(N):
			Z[i] = X[i] * (Y[i].real - Y[i].imag * 1j) #Y*
		z = np.fft.ifft(x)
		K = lambda m:  (math.abs(z[m]) if m >= 0 else z[N - math.abs(m)])
	return K
	
def xy_SPM(x, y, L):
	sum1 = 0
	sum2 = 0
	N1 = len(x)
	N2 = len(y)
	for i in range(N1):
		sum1 += x[i]
	sum1 /= N1
	for i in range(N2):
		sum2 += y[i]
	sum2 /= N2
	N = math.pow(2, math.ceil(math.log(2 * max(N1, N2), 2)))
	for i in range(N1, N):
		x.append(sum1)
	for i in range(N2, N):
		y.append(sum2)
	X = FFT(x)
	Y = FFT(y)
	G = []
	for k in range(N):
		G.append((X[k].real - X[k].imag * 1j) * Y[k])
	G1 = []
	for k in range(N):
		G1.append(0)
		for l in range(-L, L + 1):
			G1[k] += G[(k + L) % N]
		G1[k] /= 2 * L + 1
	return G1

def xy_SPM_to_Real(P, ind, Gx, Gy):
	res = []
	for i in range(len(P)):
		if ind == 1:
			res.append(P[i].real)
		elif ind == 2:
			res.append(P[i].imag)
		elif ind == 3:
			res.append(math.sqrt(P[i].real * P[i].real + P[i].imag * P[i].imag))
		elif ind == 4:
			res.append(math.arctan(math.abs((P[i].imag + 0.0) / P[i].real)))
		elif ind == 5:
			res.append((P[i].real * P[i].real + P[i].imag * P[i].imag) / (Gx[k] * Gy[k]))
		elif ind == 6:
			res.append(math.sqrt(P[i].real * P[i].real + P[i].imag * P[i].imag) / Gx[k])
	return res


class Lab4(Labs_):
	generatedSignal = QtCore.pyqtSignal()
	analyzedSignal = QtCore.pyqtSignal()

	def __init__(self, parent):
		super(Lab4, self).__init__(parent, 1)
		self.parent = parent

		self.verticalLayout = QtGui.QHBoxLayout(self)
		self.setLayout(self.verticalLayout)
		
		self.sc1 = MyStaticMplCanvas(self, width=1000, height=1000, dpi=100)
		self.sc2 = MyStaticMplCanvas(self, width=1000, height=1000, dpi=100)
		self.sc3 = MyStaticMplCanvas(self, width=1000, height=1000, dpi=100)
		self.sc4 = MyStaticMplCanvas(self, width=1000, height=1000, dpi=100)

		self.sc2.axes.hold(True)
		self.sc3.axes.hold(True)
		
		tabWidget = QtGui.QTabWidget(self)
		self.verticalLayout.addWidget(tabWidget)
		tabWidget.addTab(self.sc1, u'Сигнал')
		tabWidget.addTab(self.sc2, u'Амплитудный и фазовый спектры')
		tabWidget.addTab(self.sc3, u'Амплитудный спектр')
		tabWidget.addTab(self.sc4, u'Фазовый спектр')

		self.resultsLabel = QtGui.QLabel('')

		layout = QtGui.QVBoxLayout(self)
		self.verticalLayout.addLayout(layout)
		
		self.solLayout = QtGui.QGridLayout(self)
		layout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
		layout.addLayout(self.solLayout)

		self.solLayout.addWidget(self.resultsLabel, 0, 0)

		#label = QtGui.QLabel(u'Источник выборки')
		#self.solLayout.addWidget(label, 0, 0)
		#self.source = QtGui.QComboBox(self)
		#self.solLayout.addWidget(self.source, 0, 1)
		#self.source.addItems([u'Сгенерировать', u'Загрузить из файла'])
		#self.source.currentIndexChanged.connect(self.changeControlsVisibility)
		
		#self.selectFile = QtGui.QPushButton(self)
		#self.selectFile.setText(u'Выбрать файл')
		#self.solLayout.addWidget(self.selectFile, 1, 0)
		#self.selectFile.clicked.connect(self.selectFilePressed)
		
		label = QtGui.QLabel(u'Количество отсчетов')
		self.solLayout.addWidget(label, 2, 0)
		self.expNum = QtGui.QSpinBox(self)
		self.solLayout.addWidget(self.expNum, 2, 1)
		self.expNum.setRange(1, 1000000000)
		self.expNum.setValue(100)
		self.expNum.valueChanged.connect(self.changed)
		
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
	
		self.doDFT = QtGui.QPushButton(self)
		self.doDFT.setText(u'Дискретное преобразование Фурье')
		self.doDFT.clicked.connect(self.DFT)
		self.solLayout.addWidget(self.doDFT, 6, 0)		
			
		self.isGenerated = False	
		self.parameters = None	
		self.results = None
		self.changeControlsVisibility()

		self.signalsCombobox = QtGui.QComboBox(self)
		self.signalsCombobox.currentIndexChanged.connect(self.signalsComboboxChanged)
		self.solLayout.addWidget(self.signalsCombobox, 7, 0)

		self.signalLayouts = []
		for i in range(12):
			layout = QtGui.QGridLayout(self)
			signal = globals()['DigitalSignal{0}'.format(i + 1)](0, self)
			layout = signal.fillLayout(layout)
			self.signalLayouts.append(layout)
			self.solLayout.addLayout( layout, 10, 0)
			for j in range(layout.count()):
				layout.itemAt(j).widget().setVisible(False)
			if i == 11:
				global signal12
				signal12 = signal

		for i in range(12):
			self.signalsCombobox.addItem(str(i + 1))

		label = QtGui.QLabel(u'Режим отображения')
		self.solLayout.addWidget(label, 8, 0)
		self.graphType = QtGui.QComboBox(self)
		self.graphType.currentIndexChanged.connect(self.graphTypeChanged)
		self.solLayout.addWidget(self.graphType, 8, 1)
		self.graphType.addItem(u'Классический')
		self.graphType.addItem(u'В виде ломаной')

		self.hideSignalLayouts(0)

	def changed(self):
		self.resultsLabel.setText('')
		self.isGenerated = False	
		self.parameters = None	
		self.results = None
		self.changeControlsVisibility()
		self.sc1.clear()
		self.sc2.clear()
		self.sc3.clear()
		self.sc4.clear()
		self.isGeneratedLabel.setText(u'Сигнал не сгенерирован')

	def hideSignalLayouts(self, index):
		self.sc1.clear()
		self.resultsLabel.setText('')
		for i in range(12):
			layout = self.signalLayouts[i]
			for j in range(layout.count()):
					layout.itemAt(j).widget().setVisible(i == index)
	
	def signalsComboboxChanged(self, index):
		self.hideSignalLayouts(index)
		self.isGenerated = False	
		self.parameters = None	
		self.results = None
		self.changeControlsVisibility()
		self.sc1.clear()
		self.sc2.clear()
		self.sc3.clear()
		self.sc4.clear()

	def draw(self):
		if (self.graphType.currentIndex() ==0 ):	
			self.sc1.vlines(range(self.N), [0 for i in range(self.N)], self.u)
		else:
			self.sc1.plot(range(self.N), self.u, '-', 'red')

	def graphTypeChanged(self, index):
		self.sc1.clear()
		if (self.isGenerated):
			self.draw()

	def selectFilePressed(self):
		fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',  os.getcwd())
		if os.path.isfile(fname):
			self.isGeneratedLabel.setText(u'Загружается сигнал...')
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
				self.isGeneratedLabel.setText(u'Сигнал загружен')			
			except:
				self.isGeneratedLabel.setText(u'Сигнал не сгенерирован')
				showMessage(u'Ошибка', u'Некорректный формат файла')

	def generated(self):
		self.isGeneratedLabel.setText(u'Сигнал сгенерирован')
		self.isGenerated = True
		self.changeControlsVisibility()
		self.parent.changeState('')
		if not self.dontSave.isChecked():
			f = open('DigitalSignal{0}.dat'.format(self.signalsCombobox.currentIndex() + 1), 'w')
			f.write('1\n')
			f.write('DigitalSignal{0}\n'.format(self.signalsCombobox.currentIndex() + 1))
			f.write('1 %s 1\n' % self.N)
			for u in self.u:
				f.write('%s\n' % u)
			f.close()

	def analyzed(self):
		self.changeControlsVisibility()
		self.parent.changeState('')
			
	def startGenerate(self):
		self.changeControlsVisibility()
		self.N = self.expNum.value()
		index = self.signalsCombobox.currentIndex() 
		signal = globals()['DigitalSignal{0}'.format(index + 1)](self.N, self)
		signal.getDataFromLayout(self.signalLayouts[index])
		self.u = signal.generate()
		self.isGenerated = True
		self.draw()
		self.generatedSignal.emit()		
		
	def countStatParams(self):
		m = 0
		for u in self.u:
			m += u
		m = (m  + 0.0)/ self.N
		sigma_2 = 0
		gamma = 0
		kapa = 0
		for u in self.u:
			sigma_2 += math.pow(u - m, 2)
			gamma += math.pow(u - m, 3)
			kapa += math.pow(u - m, 4)
			
		sigma_2 = sigma_2 / (self.N - 1.0)
		sigma = math.sqrt(sigma_2)
		try:
			r = sigma / m
		except:
			r = 'inf'
		try:
			gamma = gamma / self.N / math.pow(sigma, 3)
			kapa = kapa / self.N / math.pow(sigma_2, 2) - 3
		except:
			gamma = 'inf'
			kapa = 'inf'
		self.resultsLabel.setText(u' Среднее: %s,\n Дисперсия: %s,\n Среднеквадратичное отклонение: %s,\n Коэффициент вариации: %s,\n Коээффициента асимметрии: %s,\n Коэффициент эксцесса: %s' % (
			m, sigma_2, sigma, r, gamma, kapa))
		self.analyzedSignal.emit()		
		
	def generate(self):
		self.isGeneratedLabel.setText(u'Сигнал не сгенерирован')
		self.results = None
		self.parent.changeState(u'Выполняется...')
		thread = labThread4(self, self.startGenerate)
		thread.start()

	def changeControlsVisibility(self):
		self.calc.setDisabled(not self.isGenerated)
		self.doDFT.setDisabled(not self.isGenerated)
		
	def count(self):
		self.analyzeCnt = 0;
		self.parent.changeState(u'Анализируется...')
		self.resultsLabel.setText('')
		thread2 = labThread4(self, self.countStatParams)
		thread2.start()

	def DFT(self):
		if not self.isGenerated:
			return
		self.dft = np.fft.fft(self.u)
		#DFT(self.u)
		a = []
		p = []
		for d in self.dft:
			a.append(np.abs(d))
			p.append(math.atan2(d.imag, d.real))
			
		self.sc2.clear()
		self.sc2.axes.plot(range(self.N), a, '-', label = u"амплитудный спектр")
		self.sc2.axes.plot(range(self.N), p, '-', label = u'фазовый спектр')
		self.sc2.axes.legend( (u'амплитудный спектр', u'фазовый спектр') )
		self.sc3.axes.relim()
		self.sc2.axes.margins(0.1, 0.1)
		self.sc2.draw()

		self.sc3.clear()
		self.sc3.axes.plot(range(self.N), a, '-')
		self.sc3.axes.relim()
		self.sc3.axes.margins(0.3, 0.3)
		self.sc3.draw()

		self.sc4.clear()
		#self.sc4.axes.axis(ymin = minp - delta, ymax = maxp + delta)
		self.sc4.axes.plot(range(self.N), p, '-')
		self.sc4.axes.relim()
		self.sc4.axes.margins(0.1, 0.1)
		self.sc4.draw()

