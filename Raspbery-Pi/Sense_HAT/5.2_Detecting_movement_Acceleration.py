#taking value of acceleration

from sense_hat import SenseHat
sense = SenseHat()
while True:
	acceleration = sense.get_accelerometer_raw()
		
	x = acceleration['x']
	y = acceleration['y']
	z = acceleration['Z']   #Gets the amount of gravitatio-foce acting on each axis
	x = round (x,0)
	y = round (y,0)
	z = round (z,0)
	print("x={0}, y={1}, z={2}".format(x,y,z))
