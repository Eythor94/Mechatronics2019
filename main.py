# Import programs for specific 
import GPS# GPS
import fileinput # Read/whrite files
import commands # For running Terminal comands from python code
import time
import serial
import Adafruit_BBIO.UART as UART
# Setup GPS
myGPS = GPS.GPS()
try:
        commands.getstatusoutput('cp GPS_Template.KML GPS_log.KML')
except:
        print("Not able to copy template")
        
print("DataLoging is active")
while(True):
    data = myGPS.read()
    print(data)
    
   