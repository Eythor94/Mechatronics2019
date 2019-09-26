import Adafruit_BBIO.ADC as ADC
import time
 
sensor_pin = 'P9_40'
 
ADC.setup()
while True:
    avrg = 0
    avrgTemp = 0
    for x in range(100):
        reading = ADC.read(sensor_pin)
        millivolts = (reading * 1800)*2.8277  # 1.8V reference = 1800 mV
        temp_c = (millivolts - 522) / 10
        #print('mv=%d C=%d' % (millivolts, temp_c))
        avrg = avrg + temp_c
    avrgTemp = avrg/(x+1)
    avrgTemp = round(avrgTemp, 2)
    print(avrgTemp)
    time.sleep(5)
