# Simple demo of of the ADXL345 accelerometer library.  Will print the X, Y, Z
# axis acceleration values every half second.
# Author: Tony DiCola
# License: Public Domain
import time
# Import the ADXL345 module.
import Adafruit_ADXL345

# Create an ADXL345 instance.
# Accel = Adafruit_ADXL345.ADXL345()

# Address=0x18, busnum=1
# Alternatively you can specify the device address and I2C bus with parameters:
accel = Adafruit_ADXL345.ADXL345(address=0x53, busnum=2)

_REG_INT_ENABLE          = 0x2E # Interrupt enable control
_REG_INT_MAP             = 0x2F # Interrupt mapping control
_REG_INT_SOURCE          = 0x30 # Source of interrupts, INT1 Register
_REG_THRESH_FF           = 0x28 # Free-fall threshold
_REG_TIME_FF             = 0x29 # Free-fall time

_INT_ACT                 = 0b00010000 # ACT bit
_INT_INACT               = 0b00001000 # INACT bit
_INT_FREE_FALL           = 0b00000100 # FREE_FALL  bit
# You can optionally change the range to one of:
#  - ADXL345_RANGE_2_G   = +/-2G (default)
#  - ADXL345_RANGE_4_G   = +/-4G
#  - ADXL345_RANGE_8_G   = +/-8G
#  - ADXL345_RANGE_16_G  = +/-16G
# For example to set to +/- 16G:
#accel.set_range(Adafruit_ADXL345.ADXL345_RANGE_16_G)
# Or change the data rate to one of:
#  - ADXL345_DATARATE_0_10_HZ = 0.1 hz
#  - ADXL345_DATARATE_0_20_HZ = 0.2 hz
#  - ADXL345_DATARATE_0_39_HZ = 0.39 hz
#  - ADXL345_DATARATE_0_78_HZ = 0.78 hz
#  - ADXL345_DATARATE_1_56_HZ = 1.56 hz
#  - ADXL345_DATARATE_3_13_HZ = 3.13 hz
#  - ADXL345_DATARATE_6_25HZ  = 6.25 hz
#  - ADXL345_DATARATE_12_5_HZ = 12.5 hz
#  - ADXL345_DATARATE_25_HZ   = 25 hz
#  - ADXL345_DATARATE_50_HZ   = 50 hz
#  - ADXL345_DATARATE_100_HZ  = 100 hz (default)
#  - ADXL345_DATARATE_200_HZ  = 200 hz
#  - ADXL345_DATARATE_400_HZ  = 400 hz
#  - ADXL345_DATARATE_800_HZ  = 800 hz
#  - ADXL345_DATARATE_1600_HZ = 1600 hz
#  - ADXL345_DATARATE_3200_HZ = 3200 hz
# For example to set to 6.25 hz:
#accel.set_data_rate(Adafruit_ADXL345.ADXL345_DATARATE_200_HZ)

print('Printing X, Y, Z axis values, press Ctrl-C to quit...')

accel.enable_freefall_detection()
#accel.disable_freefall_detection()

print(accel.int_read(_REG_INT_SOURCE))
int_data = 0x00

int_data = accel.int_read(_REG_INT_SOURCE)
print(int_data)
time.sleep(5)

while True:
    # Read the X, Y, Z axis acceleration values and print them.
    x, y, z = accel.read()
    #print('X={0}, Y={1}, Z={2}'.format(x, y, z))
    gx, gy, gz = accel.acceleration()
    #print('X={0}, Y={1}, Z={2}'.format(gx, gy, gz))
    # Wait half a second and repeat.
    int_data = accel.int_read(_REG_INT_SOURCE) # it's resets if read
    print(int_data)
    if (int_data-130) == 4 or (int_data-2) == 4:
        print('FALL')
        break
    time.sleep(100)
    
    #time.sleep(0.5)
    
    
    
    
    
