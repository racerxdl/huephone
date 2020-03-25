import machine, time

COMMAND_MODE=0
DATA_MODE=1

CMD_SOFT_RESET = "\x01"
CMD_SLEEP_OUT = "\x11"
CMD_SET_COLOR_MODE = "\x3A"
CMD_DISPLAY_ON = "\x29"
CMD_FRAME_RATE = "\xB1"
CMD_MADCTL = "\x08"
CMD_MADCTL_BGR = "\x08"
CMD_MADCTL_MH = "\x04"

CMD_FRMCTR1 = "\xB1"
CMD_FRMCTR2 = "\xB2"
CMD_FRMCTR3 = "\xB3"
CMD_INVCTR = "\xB4"
CMD_DISSET5 = "\xB6"

CMD_PWCTR1 = "\xC0"
CMD_PWCTR2 = "\xC1"
CMD_PWCTR3 = "\xC2"
CMD_PWCTR4 = "\xC3"
CMD_PWCTR5 = "\xC4"
CMD_VMCTR1 = "\xC5"

CMD_PWCTR6 = "\xFC"

CMD_GMCTRP1 = "\xE0"
CMD_GMCTRN1 = "\xE1"
COLOR_12BIT = "\x03"
COLOR_16BIT = "\x05"
COLOR_18BIT = "\x06"

CMD_SLPIN = "\x10"
CMD_SLPOUT = "\x11"
CMD_PTLON = "\x12"
CMD_NORON = "\x13"

CMD_INVOFF = "\x20"
CMD_INVON = "\x21"
CMD_DISPOFF = "\x28"
CMD_DISPON = "\x29"
CMD_CASET = "\x2A"
CMD_RASET = "\x2B"
CMD_RAMWR = "\x2C"

class LCD:
  '''
    ST7735 Controller Class
  '''
  def __init__(self, spi, cs, dc, reset, blk):
    self.spi = spi
    self.cs = cs
    self.dc = dc
    self.reset = reset
    self._blk = machine.PWM(blk)
    
    self._blk.freq(500)
    self._blk.duty(1023)
    self.reset()
  
  def set_backlight_brightness(self, brightness):
    '''
      Sets LCD Brightness in percent
    '''
    print("Setting brightness to %d%%" %brightness)
    bright = brightness / 100.0
    bright = bright * 1023
    self._blk.duty(int(bright))
    
  def _wait(self):
    time.sleep(0.05)
    
  def _enable(self):
    self.cs.value(0)
  
  def _disable(self):
    self.cs.value(1)

  def _cmdmode(self):
    self.dc.value(COMMAND_MODE)
  
  def _datmod(self):
    self.dc.value(DATA_MODE);
   
  def _cmd(self, cmd):
    self._enable()
    self._cmdmode()
    self.spi.write(cmd)
   
  def _data(self, data):
    self._enable()
    self._datmod()
    self.spi.write(data)
    
  def start_display(self):
    self._enable()
    self._cmd(CMD_SOFT_RESET)
    time.sleep(0.5)
    
    self._cmd(CMD_SLPOUT)
    time.sleep(0.5)
    
    self._cmd(CMD_SET_COLOR_MODE)
    self._data(COLOR_12BIT)
    time.sleep_us(10)
    
    self._cmd(CMD_FRMCTR1)
    self._data("\x00\x06\x03")
    time.sleep_us(10)
    
    self._cmd(CMD_INVCTR)
    self._data("\x00")
    
    self._cmd(CMD_PWCTR1)
    self._data("\x02\x70")
    time.sleep_us(10)
    
    self._cmd(CMD_PWCTR2)
    self._data("\x05")
    
    self._cmd(CMD_PWCTR3)
    self._data("\x01\x02")
    
    self._cmd(CMD_VMCTR1)
    self._data("\x3C\x38")
    time.sleep_us(10)
    
    self._cmd(CMD_PWCTR6)
    self._data("\x11\x15")
   
    self._cmd(CMD_CASET)
    self._data("\x00\x02\x00\0x9F")
    self._cmd(CMD_RASET)
    self._data("\x01\x4F")
    
    self._cmd(CMD_NORON)
    time.sleep_us(10)
    
    self._cmd(CMD_RAMWR)
    time.sleep_us(500)
    
    self._cmd(CMD_DISPLAY_ON)
    time.sleep_us(50)
    self.draw()
    self._disable()
  
  def draw(self):
    self._cmd(CMD_RAMWR)
    self._datmod()
    for i in range(6400):
      self.spi.write("\xf0\xff\ff")
  
  def reset(self):
    self.dc.value(0)
    # Reset Device
    self.reset.value(1)
    time.sleep(0.05)
    self.reset.value(0)
    time.sleep(0.05)
    self.reset.value(1)
    time.sleep(0.05)
    
  
  def update(self):
    pass

