from PyQt4 import QtGui
import sys
import os
import time
import urllib2
import numpy as np
import picamera
import picamera.array
import scipy.optimize as opt
from scipy.stats import norm
from matplotlib import pyplot as plt
from matplotlib import dates, ticker

class BeamProfiler(QtGui.QWidget):

	def __init__(self):
		super(BeamProfiler, self).__init__()
        	self.initializeGUI()

	def initializeGUI(self):
		'''Initializes GUI
		'''
		self.setGeometry(400, 150, 350, 550)
		self.setWindowTitle('Beam Profiler')
		layout = QtGui.QGridLayout()
		from matplotlib import pyplot as plt
		captureimage  = QtGui.QPushButton('Capture Image')
		get1DnormX    = QtGui.QPushButton('Show a 1D Gaussian in the X')
		get1DnormY    = QtGui.QPushButton('Show a 1D Gaussian in the Y')
		get2Dnorm     = QtGui.QPushButton('Show a 2D Gaussian')
		#changeres     = QtGui.QPushButton('Change Resolution')
		
		captureimage.clicked.connect(self.captureimage)
		get1DnormX.clicked.connect(self.norm1D('x'))
		get1DnormY.clicked.connect(self.norm1D('y'))
		get2Dnorm.clicked.connect(self.norm2D)
		#changeres.clicked.connect(self.changeres)
		
		layout.addWidget(captureimage    ,0,0)
		layout.addWidget(get1DnormX      ,1,0)
		layout.addWidget(get1DnormY      ,2,0)
		layout.addWidget(get2Dnorm       ,3,0)
		#layout.addWidget(changeres       ,5,0)
		
		self.setLayout(layout)

	def captureimage(self):
		with picamera.PiCamera() as self.camera:
			with picamera.array.PiRGBArray(camera) as self.output:
				camera.capture(output, 'rgb')
				print('Captured %dx%d image' % (self.output.array.shape[1], self.output.array.shape[0]))
				'''DATA CAPTURED-->SEND TO FIT'''
				#What do we want to fit?
				norm1D('x')
				norm1D('y')
				norm2D()

	def norm1D(self, axis):
		'''
		#Generate some data
		data = norm.rvs(10.0, 2.5, size=500)
		'''
		#Fit a normal distribution
		''' This line won't work yet, my guess is that output is a rank 2 array, first axis is X and second axis is Y, or vice-versa '''
		mu, std = norm.fit(self.output)

		#Plot the histogram
		plt.hist(data, bins=25, normed=True, alpha=0.6, color='g')

		#Plot the PDF
		xmin, xmax = plt.xlim()
		x = np.linspace(xmin, xmax, 100)
		p = norm.pdf(x, mu, std)
		plt.plot(x, p, 'k', linewidth=2)
		title = "Fit results: mu = %.2f, std = %.2f" % (mu, std)
		plt.title(title)

		plt.show()

	def norm2D(self):
		#Create x and y indices
		x = np.linspace(0, 200, 201)
		y = np.linspace(0, 200, 201)
		x, y = np.meshgrid(x, y)

		#Create data
		data = twoD_Gaussian((x, y), 3, 100, 100, 20, 40, 0, 10)
		#print data

		#Plot twoD_Gaussian data generated above
		plt.figure()
		plt.imshow(data.reshape(201, 201))
		plt.colorbar()

		#Add some noise to the data and try to fit the data generated beforehand
		initial_guess = (3, 100, 100, 20, 40, 0, 10)

		data_noisy = data + 0.2*np.random.normal(size=data.shape)

		popt, pcov = opt.curve_fit(twoD_Gaussian, (x, y), data_noisy, p0=initial_guess)
		#print popt

		#Plot the results
		data_fitted = twoD_Gaussian((x, y), *popt)

		fig, ax = plt.subplots(1, 1)
		ax.hold(True)
		ax.imshow(data_noisy.reshape(201, 201), cmap=plt.cm.jet, origin='bottom', extent=(x.min(), x.max(), y.min(), y.max()))
		ax.contour(x, y, data_fitted.reshape(201, 201), 8, colors='w')

		plt.show()


	def sumColRow(self, data, choice):
		"""This will sum over the column or the row"""
		result = data.sum(axis=choice)
		#print(result)
		return result

	#define model function and pass independent variables x and y as a list
	def twoD_Gaussian(self, (x,y), amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
        	xo = float(xo)
        	yo = float(yo)
        	a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
        	b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
        	c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
        	g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) + c*((y-yo)**2)))

	        return g.ravel()



if __name__ == "__main__":
    a = QtGui.QApplication([])
    beamWidget = BeamProfiler()
    beamWidget.show()
    sys.exit(a.exec_())
