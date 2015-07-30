import XP_g2d as g2d
from beam_profiler_XP import BeamProfiler as bp
from matplotlib import pylab as pylab

shutter = 2000
a_pixel = 2592
b_pixel = 1944
a_res = 100
b_res = 100

b=bp()
b.take_image(a_res, b_res, shutter)
b.image.show()

G2D = g2d.Gaussian2D(b.array, rho=50, x0=30, y0=20, w_a=9, w_b=7)
print 'w_a = ', G2D.w_a_len, 'm'
print 'w_b = ', G2D.w_b_len, 'm'

row_sum = [sum(b.array[:,i]) for i in xrange(len(b.array[0]))]
col_sum = [sum(b.array[i,:]) for i in xrange(len(b.array[1]))]
pylab.plot(row_sum)
pylab.plot(col_sum)
pylab.show()
