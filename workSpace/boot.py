
from machine import I2C,Pin,SPI
import time, os
import _thread

import ip5306, st7735

LCD_RESET = Pin(4, Pin.OUT)
LCD_DC = Pin(25, Pin.OUT)
LCD_CS = Pin(14, Pin.OUT)
LCD_BLK = Pin(33, Pin.OUT)

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
vspi = SPI(2, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

led = Pin(13, Pin.OUT)
ip5306.KeepBoostPowerOn(i2c)


print("Hello world, HUEHEUEHUE")
lcd = st7735.LCD(vspi, LCD_CS, LCD_DC, LCD_RESET, LCD_BLK)
lcd.set_backlight_brightness(100)
lcd.start_display()

#running = True

#def LedBlink():
#  while running:
#    led.value(0)
#    time.sleep(1)
#    led.value(1)
#    time.sleep(1)

#huebr = _thread.start_new_thread(LedBlink, ())



