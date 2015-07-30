import time
import picamera
import picamera.array
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

with picamera.PiCamera() as camera:
	with picamera.array.PiRGBArray(camera) as output:
		#output is a 3D array with (rows, columns, colors)
		camera.capture(output, 'rgb')
		camera.flush()
		print('Captured %dx%d image' % (output.array.shape[1], output.array.shape[0]))
		print(output.array.shape)
		print type(output)
		#imgplot = plt.imshow(output)
		
