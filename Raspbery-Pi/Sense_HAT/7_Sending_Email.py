#sending to email (make it as Email.py)

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from sense_hat import SenseHat
import time
from time import asctime

sense=SenseHat()

fromaddr = "edurekatest11@gmail.com"
toaddr ="edurekaraspberrypi@gmai.com"
msg =MIMEMultipart()
msg['From'] =fromaddr
msg['To'] = toaddr
msg['Subject'] = "Temp Rasp"

temp=round(sense.get_tempurature()*1.8 +32)
humidity = round(sense.get_humidity())
pressure = round(sense.get_pressure())
message =" T=%dF, H=%d, P=%d" %(temp.humidity.pressure)
print(message)
msg.attach(MIMEText(message, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 25) # port
server.starttls()
server.login(fromaddr, "#password_here")
text = msg.as_string()
server.sendmail(fromaddr,toaddr, text)
server.quit()
