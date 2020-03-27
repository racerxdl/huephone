import machine, time, binascii

COMMAND_MODE=0
DATA_MODE=1

CMD_SOFT_RESET = [0x01]
CMD_SLEEP_OUT = [0x11]
CMD_SET_COLOR_MODE = [0x3A]
CMD_DISPLAY_ON = [0x29]
CMD_MADCTL = [0x36]

CMD_FRMCTR1 = [0xB1]
CMD_FRMCTR2 = [0xB2]
CMD_FRMCTR3 = [0xB3]
CMD_INVCTR = [0xB4]
CMD_DISSET5 = [0xB6]

CMD_PWCTR1 = [0xC0]
CMD_PWCTR2 = [0xC1]
CMD_PWCTR3 = [0xC2]
CMD_PWCTR4 = [0xC3]
CMD_PWCTR5 = [0xC4]
CMD_VMCTR1 = [0xC5]

CMD_PWCTR6 = [0xFC]

CMD_GMCTRP1 = [0xE0]
CMD_GMCTRN1 = [0xE1]
COLOR_12BIT = [0x03]
COLOR_16BIT = [0x05]
COLOR_18BIT = [0x06]

CMD_SLPIN = [0x10]
CMD_SLPOUT = [0x11]
CMD_PTLON = [0x12]
CMD_NORON = [0x13]

CMD_INVOFF = [0x20]
CMD_INVON = [0x21]
CMD_DISPOFF = [0x28]
CMD_DISPON = [0x29]
CMD_CASET = [0x2A]
CMD_RASET = [0x2B]
CMD_RAMWR = [0x2C]


def TFTColor( aR, aG, aB ) :
  '''Create a 16 bit rgb value from the given R,G,B from 0-255.
     This assumes rgb 565 layout and will be incorrect for bgr.'''
  return ((aR & 0xF8) << 8) | ((aG & 0xFC) << 3) | (aB >> 3)

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
    self.cs(1)
  
  def set_backlight_brightness(self, brightness):
    '''
      Sets LCD Brightness in percent
    '''
    print("Setting brightness to %d%%" %brightness)
    bright = brightness / 100.0
    bright = bright * 1023
    self._blk.duty(int(bright))
  
  def _cmd(self, cmd):
    self.dc(0)
    self.cs(0)
    self.spi.write(bytearray(cmd))
    #print("CMD", binascii.hexlify(bytearray(cmd)))
    self.cs(1)
   
  def _data(self, data):
    self.dc(1)
    self.cs(0)
    self.spi.write(bytearray(data))
    #print("DATA", binascii.hexlify(bytearray(data)))
    self.cs(1)
    
  def start_display(self):
    print("Starting display")
    self.reset()
    
    self._cmd(CMD_SOFT_RESET)
    time.sleep_us(150)
    
    self._cmd(CMD_SLPOUT)
    time.sleep_us(500)
    
    self._cmd(CMD_FRMCTR1)
    self._data([0x01, 0x2C, 0x2D])
    
    self._cmd(CMD_FRMCTR2)
    self._data([0x01, 0x2C, 0x2D])
    
    self._cmd(CMD_FRMCTR3)
    self._data([0x01, 0x2C, 0x2D, 0x01, 0x2C, 0x2D])
    time.sleep_us(10)
   
    self._cmd(CMD_INVCTR)
    self._data([0x07])
    
    
    self._cmd(CMD_PWCTR1)
    self._data([0xA2, 0x02, 0x84])
    
    self._cmd(CMD_PWCTR2)
    self._data([0xC5])
    
    self._cmd(CMD_PWCTR3)
    self._data([0x0A, 0x00])
    
    self._cmd(CMD_PWCTR4)
    self._data([0x8A, 0x2A])
    
    self._cmd(CMD_PWCTR5)
    self._data([0x8A, 0xEE])
    
    self._cmd(CMD_VMCTR1)
    self._data([0x0E])
    
    self._cmd(CMD_INVOFF)
    
    self._cmd(CMD_MADCTL)
    self._data([0xC8])
        
    self._cmd(CMD_SET_COLOR_MODE)
    self._data([0x05])    
    
    self._cmd(CMD_CASET)
    self._data([0x00, 0x00, 0x00, 0x7F])
    self._cmd(CMD_RASET)
    self._data([0x00, 0x00, 0x00, 0x9F])
    
    
    self._cmd(CMD_GMCTRP1)
    self._data([0x0f, 0x1a, 0x0f, 0x18, 0x2f, 0x28, 0x20, 0x22, 0x1f,
                            0x1b, 0x23, 0x37, 0x00, 0x07, 0x02, 0x10])
    
    self._cmd(CMD_GMCTRN1)
    self._data([0x0f, 0x1b, 0x0f, 0x17, 0x33, 0x2c, 0x29, 0x2e, 0x30,
                            0x30, 0x39, 0x3f, 0x00, 0x07, 0x03, 0x10])
    time.sleep_us(10)
    
    self._cmd(CMD_DISPLAY_ON)
    time.sleep_us(100)
    
    self._cmd(CMD_NORON)
    time.sleep_us(10)
    
    self.cs(1)
    
    self.draw()
  
  def _write_pixels(self, pixels):
    self.dc(1)
    self.cs(0)
        
    for i in range(pixels//32):
      #print("WDATA", binascii.hexlify(bytearray(self._color)))
      self.spi.write(self._color)
    
    self.cs(1)
  
  def draw(self):
    print("Drawing on screen")
    self._cmd(CMD_CASET)
    self._data([0x00, 0x00, 0x00, 0x7F])
    self._cmd(CMD_RASET)
    self._data([0x00, 0x00, 0x00, 0x9F])
    self._cmd(CMD_RAMWR)
    
    c = TFTColor(0xFF, 0xFF, 0x00)
    b0 = c >> 8
    b1 = c & 0xFF
    self._color = bytes([b0, b1]) * 32
    self._write_pixels(160*80)
    self.cs(1)
  
  def reset(self):
    print("Resetting display")
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




