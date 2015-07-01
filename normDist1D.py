import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

#Generate some data
data = norm.rvs(10.0, 2.5, size=500)
#print data

#Fit a normal distribution
mu, std = norm.fit(data)

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
