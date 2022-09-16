#code: (sensing the environment)

from sense_hat import SenseHat
sense = SenseHat()
while True:
	t=sense.get_tempurature()
	p=sense.get_pressure()
	h=sense.get_humidity() #getting tempurature, humidity & pressure
	t=round(t,1)
	p=round(p,1)
	h=round(h,1)  #rounding to 1 decimal point

	if t > 36:
		bg=[0,100,0]  #green
		tc=[255,255,255] #white
	else:
		bg=[0,0,100] #blue
		tc=[200,200,0] #yellow

	msg ="Tempurature ={0}, Pressure ={1}, Humidity={2}".format(t,p,h)
	sense.show_message(msg,scroll_speed=0.05,text_colour=tc, back_colour=bg)
