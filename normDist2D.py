import scipy.optimize as opt
import numpy as np
import pylab as plt

#define model function and pass independent variables x and y as a list
def twoD_Gaussian((x,y), amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
	xo = float(xo)
	yo = float(yo)
	a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
	b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
	c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
	g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) + c*((y-yo)**2)))
	
	return g.ravel()

#Create x and y indices
x = np.linspace(0, 1079, 1080)
#print x
y = np.linspace(0, 1079, 1080)
#print y
x, y = np.meshgrid(x, y)

#Create data
data = twoD_Gaussian((x, y), 20, 540, 540, 100, 200, 0, 10)
print data

#Plot twoD_Gaussian data generated above
plt.figure()
plt.imshow(data.reshape(1080, 1080))
plt.colorbar()

#Add some noise to the data and try to fit the data generated beforehand
initial_guess = (20, 540, 540, 100, 200, 0, 10)

data_noisy = data + 0.2*np.random.normal(size=data.shape)

popt, pcov = opt.curve_fit(twoD_Gaussian, (x, y), data_noisy, p0=initial_guess)
#print popt

#Plot the results
data_fitted = twoD_Gaussian((x, y), *popt)

fig, ax = plt.subplots(1, 1)
ax.hold(True)
ax.imshow(data_noisy.reshape(1080, 1080), cmap=plt.cm.jet, origin='bottom', extent=(x.min(), x.max(), y.min(), y.max()))
ax.contour(x, y, data_fitted.reshape(1080, 1080), 8, colors='w')

plt.show()
