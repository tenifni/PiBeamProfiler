import picamera
import picamera.array

with picamera.PiCamera() as camera:
	with picamera.array.PiRGBArray(camera) as output:
		#output is a 3D array with (rows, columns, colors)
		camera.capture(output, 'rgb')
		print('Captured %dx%d image' % (output.array.shape[1], output.array.shape[0]))
