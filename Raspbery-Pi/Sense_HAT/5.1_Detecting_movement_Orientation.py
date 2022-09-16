#code:(detecting movement)

#taking value of orientation

from sense_hat import SenseHat
sense = SenseHat()
while True:
	orientation = sense.get_orientation() #Getting orientation using gyroscope
	
	pitch = orientation['pitch'] 
	roll = orientation['roll']
	yaw = orientation['raw']  #getting pitch, roll, yaw

	print("pitch={0}. roll={1}, yaw={2}".format(pitch,yaw,roll))


