
from machine import I2C,Pin,SPI
import time, os
import _thread

import ip5306

from st7735 import TFT, TFTColor
from sysfont import sysfont

LCD_RESET = 4 	# Pin(4, Pin.OUT, Pin.PULL_DOWN)
LCD_DC = 25 	# Pin(25, Pin.OUT, Pin.PULL_DOWN)
LCD_CS = 14 	# Pin(14, Pin.OUT, Pin.PULL_DOWN)
LCD_BLK = 33 	# Pin(33, Pin.OUT)

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
vspi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

led = Pin(13, Pin.OUT)
ip5306.KeepBoostPowerOn(i2c)

tft=TFT(vspi,LCD_DC,LCD_RESET,LCD_CS, LCD_BLK)
tft._offset = (4, 28)
tft._size = (160, 160)
tft.initr()
tft.set_backlight_brightness(2)
tft.invertcolor(False)
tft.rotation(3)
tft.fill(TFTColor(0x00, 0x00, 0x00))

tft.text( (0, 0), "Teste de Margem", TFT.CYAN, sysfont, 1)

running = True

def PrintBatteryLevel():
 while running:
 	level = ip5306.GetBatteryPercent()
 	tft.text( (0, 10), "Bateria %s %%    " % level, TFT.CYAN, sysfont, 1)
	time.sleep(0.1)

batteryThread = _thread.start_new_thread(PrintBatteryLevel, ())




