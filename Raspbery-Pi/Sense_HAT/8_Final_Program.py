

import pycurl, json             # pycurl: help on establish connection of API
from StringIO import StringIO   #StringIO: a StringIO package
import RPi.GPIO as GPIO         #GPIO from Raspberry Pi
from sense_hat import SenseHat  #importing Sense Hat
import time			#for delay
from time import asctime        #importing Time

sense = senseHat()
sense.clear()  #clear data that stuck for sensors

cold=37  #notification
hot=40
pushMessage=""

#####################################
#Code for display number

OFFSET_LEFT = 1  #off 1st colum (IoT demo picture)
OFFSET_TOP = 2   #off first 2 rows

#Diplaying numbers on SenseHat: Tens Place
NUMS = [1,1,1,1,0,1,1,0,1,1,0,1,1,1,1, #0 - 3x5 matrix in IoT Demo-2 picture
	0,1,0,0,1,0,0,1,0,0,1,0,0,1,0, #1
	1,1,1,0,0,1,0,1,0,1,0,0,1,1,1, #2
	1,1,1,0,0,1,1,1,1,0,0,1,1,1,1, #3
	1,0,0,1,0,1,1,1,1,0,0,1,0,0,1, #4
	1,1,1,1,0,0,1,1,1,0,0,1,1,1,1, #5
	1,1,1,1,0,0,1,1,1,1,0,1,1,1,1, #6
	1,1,1,0,0,1,0,1,0,1,0,0,1,0,0, #7
	1,1,1,1,0,1,1,1,1,1,0,1,1,1,1, #8
	1,1,1,1,0,1,1,1,1,0,0,1,0,0,1] #9 

#Display a single digit (0-9) on SenseHat
#xd - x coordinate to where the digit has to be represent
#yd - y coordinate to where the digit has to be represent
#rgb - red green blue
#val - takes value as input(xd) , tens value

def show_digit(val, xd, yd, r, g, b):
	offset = val * 15  
#lets say val is 3 (3rd row of matrix), then 3*15 = 45 (need to move 45 position)
	for p in range(offset, offset + 15):
		xt = p % 3  #0 place, 1 place, or 2 place
		yt = (p-offset) // 3   #which column value should be take
		sense.set_pixel(xt+xd, yt+yd, r*NUMS[p], g*NUMS[p], b*NUMS[p])

#Displays a two-digit postive number (0-99) on senseHat
def show_number(val, r, g, b):
	abs_val = abs(val)
	tens = abs_val // 10
	units = abs_val % 10
	if (abs_val > 9):
		show_digit(tens, OFFSET_LEFT, OFFSET_TOP, r, g, b)
	show_digit(units, OFFSET_LEFT+4, OFFSET_TOP, r, g, b)

#---------1:44:22---------------------
################################################################

temp = round(sense.get_tempurature())
humidity = round(sense.get_humidity())
pressure = round(sense.get_pressure())
message = "T=%dC, H=%d, P=%d " %(temp,humidity, pressure)

#setup InstaPush variables
# add your Instapush Application ID
appID ="59bb6e6ba4c48a1cd674e33d"

#add your Instapush Application Secret
appSecret = "fd127d824390296b5f84818cddafeebe"
pushEvent = "TempNotify"

# use Curl to post to the Instapush API
c=pycurl.Curl()

# set API URL
c.setopt(c.URL, 'https://api.instapush.im/v1/post')

#---------1:47:00------instapush-----

#setup custom headers for authentication variables and content type
c.setopt(c.HTTPHEADER, ['x-instapush-appid: ' + appID, 'x-instapush-appscret: '+
appSecret, 'Content-Type: application/json'])

#use this to capture the response from our push API call
buffer = StringIO()

############################################################

def p(pushMessage):
	#create a dict structure for JSON data to post
	json_fields = {}
	
	# setup JSON values
	json_fields['event'] = pushEvent
	json_fields['trackers'] = {}
	json_fields['trackers']['message'] = pushMessage 
	#print(json_fields)
	postfields = json.dumps(json_fields)

	#make sure to send the JSON with post
	c.setopt(c.POSTFIELDS, postfields)
	
	#set this so we can capture the response in our buffer
	c.setopt(c.WRITEFUNCTION, buffer.write)

	#uncomment to see the post sent
	c.setopt(c.VERBOSE, True)

#----------1.53.16------------------

#setup an indefinite loop that looks for temperature
while True:
	temp = round(sense.get_temperature())
	humidity = round(sense.get_humidity())
	pressure = round(sense.get_pressure())
	message = ' T=%dC, H=%d, P=%d ' %(temp,humidity,pressure)
	time.sleep(4)
	log = open('weather.txt',"a")
	now = str(asctime())
	temp = int(temp)
	show_number(temp, 200, 0, 60)
	temp1 = temp
	
	log.write(now+''+message+'\n')
	print(message)
	log.close()
	time.sleep(5)
	
	if temp >=hot:
		pushMessage = "Its hot:  " + message
		p(pushMessage)
		c.perform()
		# capture the response from the server
		body = buffer.getvalue()
		pushMessage = ""
	
	elif temp <= cold:
		pushMessage = "Its cold: " + message
		p(pushMessage)
		c.perform()
		#capture the response from the server
		body=buffer.getvalue()
		pushMessage=""

	#print the response
	#print(body)
	
	#reset the buffer
	buffer.truncate(0)
	buffer.seek(0)

#cleanup
c.close()
GPIO.cleanup()
