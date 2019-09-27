# Import programs for specific 
import GPS# GPS
import fileinput # Read/whrite files
import commands # For running Terminal comands from python code
import time
import serial
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.ADC as ADC
import datetime
import Adafruit_ADXL345 # Import the ADXL345 module. 
# Function that reads the Temp 
def Read_Temp():
    sensor_pin = 'P9_40'
    avrg = 0
    avrgTemp = 0
    for x in range(100):
        reading = float((ADC.read(sensor_pin)))
       # print("Reading: ",reading)
        millivolts = (reading * 1810)  # 1.8V reference = 1800 mV
        temp_c = (millivolts - 500) / 10
        #scaled_temp = temp_c*1
        avrg = avrg + temp_c
    avrgTemp = avrg/(x+1)
    avrgTemp = round(avrgTemp, 2)
    return avrgTemp
# Function that reads the GPS
def Read_GPS(myGPS):
    myGPS.read()
    try:
        if myGPS.fix!=0:
            
            latDec=float(myGPS.latDeg)+float(myGPS.latMin)/60.
            lonDec=float(myGPS.lonDeg)+float(myGPS.lonMin)/60.
            #print 'Universal Time: ',myGPS.timeUTC
            #print 'You are Tracking: ',myGPS.sats,' satellites'
            #print 'My Latitude: ',myGPS.latDeg, 'Degrees ', myGPS.latMin,' minutes ', myGPS.latHem
            #print 'My Longitude: ',myGPS.lonDeg, 'Degrees ', myGPS.lonMin,' minutes ', myGPS.lonHem
            #print 'My Speed: ', myGPS.knots
            #print 'My Altitude: ',myGPS.altitude
            		
            if myGPS.lonHem=='W':
            	lonDec=(-1)*lonDec
            if myGPS.latHem=='S':
            	latDec=(-1)*latDec
            alt=myGPS.altitude
            return_strings =str(lonDec)+','+str(latDec)+','+alt
            myString=str(lonDec)+','+str(latDec)+','+alt+'\n '
                            
            for line in fileinput.FileInput('GPS_log.KML',inplace = 1):
                if "</coordinates>" in line:
                    line = line.replace(line,myString+line)
                print(line),
            return(return_strings)
    except:
        pass

# Function that reads the Accelerometer
def Read_Accelerometer():
    gx, gy, gz = accel.acceleration() #Gets the accelerometer data
    Acel = ('X={0}, Y={1}, Z={2}'.format(gx, gy, gz))
    return Acel
    
def LOG_TO_FILE(GPS = "", Acel = "", temp = ""):
    now = datetime.datetime.now()
    Time_Stamp = (now.strftime("%Y-%m-%d %H:%M:%S"))
    
    file = open("LOG_file.txt","a")
    file.write("\nTime: {}              GPS: {}                 Temp: {}                Accelerometer: {}".format(Time_Stamp,GPS,temp,Acel))
    file.close()

# Setup
ADC.setup()
UART.setup("UART1") #Opens the Uart comunication bus Nr.1
ser=serial.Serial('/dev/ttyO1',9600)
accel = Adafruit_ADXL345.ADXL345(address=0x53, busnum=2)

GPIO.setup("P8_8", GPIO.OUT)
GPIO.setup("P8_10", GPIO.OUT)
GPIO.setup("P8_12", GPIO.IN)

accel.enable_freefall_detection(8,40)  
# defult TH = 9 and TIME = 20 (The scale factor is 5 ms/LSB)
# THIS WILL TURN ON FREE-FALL MODE AND INT1 will go HIGH if TRUE(fall)
# The scale factor is 62.5 mg/LSB. Threshold 5 to 10  and The fall time 20 to 70
#accel.disable_freefall_detection() # This is to disable the freefall detect
try:
    commands.getstatusoutput('cp GPS_Template.KML GPS_log.KML') # Delete LOG-file and copy template
except:
    print("Not able to copy template")
try:
    file = open("LOG_file.txt","w") # Delete LOG-file and make new
    file.write("Log Mechatronics 1 2019 LAB-Group 17:")
    file.close()
except:
    print("Error opening file")
    
if accel.int_read(0x2E) == 0:
    print('Free fall data is DISABLED')
int_data = accel.int_read(0x30)  # READS AND RESET THE INT FLAG

myGPS = GPS.GPS()
RUN = True
while RUN == True:
    GPS_Mesurment = Read_GPS(myGPS)
    Acel = Read_Accelerometer()
    Temp_Mesurment = Read_Temp()
    LOG_TO_FILE(GPS_Mesurment,Acel,Temp_Mesurment)
    time.sleep(3)
