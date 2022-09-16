#VNC viewer
#code: (displaying text)

from sense_hat import SenseHat  #importing SenseHat
from time import sleep
from random import randint

sense = SenseHat()     #initializing SenseHat
r = randint(0,255)
sense.show_letter("e", (r,0,0))  #Displaying letter e on LED matrix
sleep(1)
r = randint(0,255)
sense.show_letter("d", (0,0,r))
sleep(1)
sense.clear()     #Clearing SenseHat LED Matrix