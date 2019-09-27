import Adafruit_BBIO.ADC as ADC
import time
 
sensor_pin = 'P9_40'
 
ADC.setup()
while True:
    avrg = 0
    avrgTemp = 0
    for x in range(1):
        reading = float(ADC.read(sensor_pin))
        volts = reading * 1.8 # gildið í volts
        print(reading)
       # volts = (reading/1024)*500 
        #temp_c = ((volts) - 0.500)
        #avrg = avrg + temp_c
   # avrgTemp = avrg/(x+1)
    #avrgTemp = round(avrgTemp, 2)
   # print('V=%d C=%d' % (volts, avrgTemp))
    time.sleep(5)