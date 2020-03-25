from machine import Pin

IP5306_ADDR = 0x75

def KeepBoostPowerOn(i2c):
  print("IP5306 Boost Power On")
  i2c.writeto_mem(IP5306_ADDR, 0x00, "\x37")

