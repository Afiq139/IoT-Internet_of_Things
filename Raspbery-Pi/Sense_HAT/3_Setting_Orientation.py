#code: (Setting Orientation)

from sense_hat import SenseHat
import time
sense = SenseHat()
Sense.show_letter("J")
angles = [0,90,180,270,0,90,180,270]   #setting angles for rotation

for r in angles:
       sense.set_rotation(r)
       time.sleep(0.5)                 #Rotating the letter
sense.clear()