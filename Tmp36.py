import Adafruit_BBIO.ADC as ADC
import time
 
sensor_pin = 'P9_40'
 
ADC.setup()
while True:
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
    print('mv=%d C=%.2f ' % (millivolts, avrgTemp))
    time.sleep(2)