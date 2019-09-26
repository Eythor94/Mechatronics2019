# Import programs for specific 
import GPS# GPS
import fileinput # Read/whrite files
import commands # For running Terminal comands from python code
import time
import serial
import Adafruit_BBIO.UART as UART

# Setup GPS
UART.setup("UART1") #Opens the Uart comunication bus Nr.1
ser=serial.Serial('/dev/ttyO1',9600)
myGPS = GPS.GPS()
# Delete LOG-file 
try:
        commands.getstatusoutput("rm GPS_log.KML")
except:
        print("Not able to delete file")
# Copy's the template file
try:
        commands.getstatusoutput('cp GPS_Template.KML GPS_log.KML')
except:
        print("Not able to copy template")
        
        
print("DataLoging is active")
while(True):
    myGPS.read()
    print myGPS.NMEA1
    print myGPS.NMEA2
    
    try:
        if myGPS.fix!=0:
            print 'Universal Time: ',myGPS.timeUTC
            print 'You are Tracking: ',myGPS.sats,' satellites'
            print 'My Latitude: ',myGPS.latDeg, 'Degrees ', myGPS.latMin,' minutes ', myGPS.latHem
            print 'My Longitude: ',myGPS.lonDeg, 'Degrees ', myGPS.lonMin,' minutes ', myGPS.lonHem
            print 'My Speed: ', myGPS.knots
            print 'My Altitude: ',myGPS.altitude
            
            latDec=float(myGPS.latDeg)+float(myGPS.latMin)/60.
            lonDec=float(myGPS.lonDeg)+float(myGPS.lonMin)/60.
            		
            if myGPS.lonHem=='W':
            	lonDec=(-1)*lonDec
            if myGPS.latHem=='S':
            	latDec=(-1)*latDec
            alt=myGPS.altitude
            myString=str(lonDec)+','+str(latDec)+','+alt+'\n '
                            
            for line in fileinput.FileInput('GPS_log.KML',inplace = 1):
                if "</coordinates>" in line:
                    line = line.replace(line,myString+line)
                print(line),
    except:
        print("No Conection")
        pass
    time.sleep(3) #Sample rate