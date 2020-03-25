IP5306_ADDR = 0x75

i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Keep IP5306 Boost Converter On
i2c.send('\x00\x37', IP5306_ADDR)

i2c.writeto(IP5306_ADDR, b'\x00\x37')

i2c.writeto(IP5306_ADDR, b'0x78')
i2c.readfrom(IP5306_ADDR, 0x1)

i2c.readfrom(IP5306_ADDR, 0x1)


i2c.writeto(IP5306_ADDR, b'0x00')
i2c.readfrom(IP5306_ADDR, 0x1)

i2c.readfrom_mem(IP5306_ADDR, 0x78, 1)

