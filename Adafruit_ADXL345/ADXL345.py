# The MIT License (MIT)
#
# Copyright (c) 2016 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import struct

# Minimal constants carried over from Arduino library
ADXL345_ADDRESS          = 0x53 # Var 0x53
ADXL345_REG_DEVID        = 0x00 # Device ID
ADXL345_REG_DATAX0       = 0x32 # X-axis data 0 (6 bytes for X/Y/Z)
ADXL345_REG_POWER_CTL    = 0x2D # Power-saving features control
ADXL345_REG_DATA_FORMAT  = 0x31
ADXL345_REG_BW_RATE      = 0x2C
ADXL345_DATARATE_0_10_HZ = 0x00
ADXL345_DATARATE_0_20_HZ = 0x01
ADXL345_DATARATE_0_39_HZ = 0x02
ADXL345_DATARATE_0_78_HZ = 0x03
ADXL345_DATARATE_1_56_HZ = 0x04
ADXL345_DATARATE_3_13_HZ = 0x05
ADXL345_DATARATE_6_25HZ  = 0x06
ADXL345_DATARATE_12_5_HZ = 0x07
ADXL345_DATARATE_25_HZ   = 0x08
ADXL345_DATARATE_50_HZ   = 0x09
ADXL345_DATARATE_100_HZ  = 0x0A # (default)
ADXL345_DATARATE_200_HZ  = 0x0B
ADXL345_DATARATE_400_HZ  = 0x0C
ADXL345_DATARATE_800_HZ  = 0x0D
ADXL345_DATARATE_1600_HZ = 0x0E
ADXL345_DATARATE_3200_HZ = 0x0F
ADXL345_RANGE_2_G        = 0x00 # +/-  2g (default)
ADXL345_RANGE_4_G        = 0x01 # +/-  4g
ADXL345_RANGE_8_G        = 0x02 # +/-  8g
ADXL345_RANGE_16_G       = 0x03 # +/- 16g

# Added
_REG_INT_ENABLE          = 0x2E # Interrupt enable control
_REG_INT_MAP             = 0x2F # Interrupt mapping control
_REG_INT_SOURCE          = 0x30 # Source of interrupts
_REG_THRESH_FF           = 0x28 # Free-fall threshold
_REG_TIME_FF             = 0x29 # Free-fall time

_INT_ACT                 = 0b00010000 # ACT bit
_INT_INACT               = 0b00001000 # INACT bit
_INT_FREE_FALL           = 0b00000100 # FREE_FALL  bit




_STANDARD_GRAVITY = 9.80665 # earth standard gravity
_ADXL345_MG2G_MULTIPLIER = 0.004

class ADXL345(object):
    """ADXL345 triple-axis accelerometer."""

    def __init__(self, address=ADXL345_ADDRESS, i2c=None, **kwargs):
        """Initialize the ADXL345 accelerometer using its I2C interface.
        """
        # Setup I2C interface for the device.
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)
        
        
        
        # Check that the acclerometer is connected, then enable it.
        if self._device.readU8(ADXL345_REG_DEVID) == 0xE5:
            self._device.write8(ADXL345_REG_POWER_CTL, 0x08)
#       else:
#            raise RuntimeError('Failed to find the expected device ID register value, check your wiring.')
        self._device.write8(_REG_INT_ENABLE, 0x0)   
        self._enabled_interrupts = {}
        self._event_status = {}
        
        
    def set_range(self, value):
        """Set the range of the accelerometer to the provided value.  Range value
        should be one of these constants:
          - ADXL345_RANGE_2_G   = +/-2G
          - ADXL345_RANGE_4_G   = +/-4G
          - ADXL345_RANGE_8_G   = +/-8G
          - ADXL345_RANGE_16_G  = +/-16G
        """
        # Read the data format register to preserve bits.  Update the data
        # rate, make sure that the FULL-RES bit is enabled for range scaling
        format_reg = self._device.readU8(ADXL345_REG_DATA_FORMAT) & ~0x0F
        format_reg |= value
        format_reg |= 0x08  # FULL-RES bit enabled
        # Write the updated format register.
        self._device.write8(ADXL345_REG_DATA_FORMAT, format_reg)

    def get_range(self):
        """Retrieve the current range of the accelerometer.  See set_range for
        the possible range constant values that will be returned.
        """
        return self._device.readU8(ADXL345_REG_DATA_FORMAT) & 0x03

    def set_data_rate(self, rate):
        """Set the data rate of the aceelerometer.  Rate should be one of the
        following constants:
          - ADXL345_DATARATE_0_10_HZ = 0.1 hz
          - ADXL345_DATARATE_0_20_HZ = 0.2 hz
          - ADXL345_DATARATE_0_39_HZ = 0.39 hz
          - ADXL345_DATARATE_0_78_HZ = 0.78 hz
          - ADXL345_DATARATE_1_56_HZ = 1.56 hz
          - ADXL345_DATARATE_3_13_HZ = 3.13 hz
          - ADXL345_DATARATE_6_25HZ  = 6.25 hz
          - ADXL345_DATARATE_12_5_HZ = 12.5 hz
          - ADXL345_DATARATE_25_HZ   = 25 hz
          - ADXL345_DATARATE_50_HZ   = 50 hz
          - ADXL345_DATARATE_100_HZ  = 100 hz
          - ADXL345_DATARATE_200_HZ  = 200 hz
          - ADXL345_DATARATE_400_HZ  = 400 hz
          - ADXL345_DATARATE_800_HZ  = 800 hz
          - ADXL345_DATARATE_1600_HZ = 1600 hz
          - ADXL345_DATARATE_3200_HZ = 3200 hz
        """
        # Note: The LOW_POWER bits are currently ignored,
        # we always keep the device in 'normal' mode
        self._device.write8(ADXL345_REG_BW_RATE, rate & 0x0F)

    def get_data_rate(self):
        """Retrieve the current data rate.  See set_data_rate for the possible
        data rate constant values that will be returned.
        """
        return self._device.readU8(ADXL345_REG_BW_RATE) & 0x0F

    def read(self):
        """Read the current value of the accelerometer and return it as a tuple
        of signed 16-bit X, Y, Z axis values.
        """
        raw = self._device.readList(ADXL345_REG_DATAX0, 6)
        return struct.unpack('<hhh', raw)
        
# ADDED BY AGNAR
        
    def acceleration(self):
        """The x, y, z acceleration values returned in a 3-tuple in m / s ^ 2."""
        x, y, z = struct.unpack('<hhh',self._device.readList(ADXL345_REG_DATAX0, 6))
        x = x * _ADXL345_MG2G_MULTIPLIER * _STANDARD_GRAVITY
        y = y * _ADXL345_MG2G_MULTIPLIER * _STANDARD_GRAVITY
        z = z * _ADXL345_MG2G_MULTIPLIER * _STANDARD_GRAVITY
        return (x, y, z)
        
    def enable_freefall_detection(self, threshold=9, time=20):
        """
        Freefall detection parameters:
        :param int threshold: The value that acceleration on all axes must be under to\
        register as dropped. The scale factor is 62.5 mg/LSB.
        :param int time: The amount of time that acceleration on all axes must be less than\
        ``threshhold`` to register as dropped. The scale factor is 5 ms/LSB. Values between 100 ms\
        and 350 ms (20 to 70) are recommended.
        If you wish to set them yourself rather than using the defaults,
        you must use keyword arguments::
            accelerometer.enable_freefall_detection(time=30)
       """

        self._device.write8(_REG_INT_ENABLE, 0x0)
        self._device.write8(_REG_THRESH_FF, threshold) # threshold 05 - 09
        self._device.write8(_REG_TIME_FF, time)    # The fall time 0x14 to 0x46
        self._device.write8(_REG_INT_ENABLE,_INT_FREE_FALL) # INT for free fall ON

    def disable_freefall_detection(self):
        "Disable freefall detection"
        self._device.write8(_REG_INT_ENABLE, 0x0)
        
        
    def write(self, reg, data):
        self._device.write8(reg, data)

    def int_read(self, reg):
        return self._device.readU8(reg)
        