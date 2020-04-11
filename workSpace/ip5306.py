from machine import Pin, ADC

IP5306_ADDR = 0x75

_batteryPin = ADC(Pin(35))
_batteryPin.atten(ADC.ATTN_11DB)
_batteryPin.width(ADC.WIDTH_12BIT)

_averageWindow = 10

_voltageVector = [3.3, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.05, 4.10, 4.15, 4.20]
_percentVector = [  0,   3,   5,   8, 36,  62,  73,   83,   89,   94,  100]
_lastPercentValues = [ 0 for x in range(_averageWindow) ]

def KeepBoostPowerOn(i2c):
  print("IP5306 Boost Power On")
  i2c.writeto_mem(IP5306_ADDR, 0x00, "\x37")

def GetBatteryVoltage():
	val = _batteryPin.read()
	# 0 -> 3.6V
	# 0 -> 4096
	return 3.6 * ((val * 2) / 4096)

def GetBatteryPercent():
	global _lastPercentValues
	voltage = GetBatteryVoltage()

	if voltage <= 3.3:
		p = 0
	elif voltage >= 4.2:
		p = 100
	else:
		vMin = 0
		vMax = 0
		vMinIdx = 0
		vMaxIdx = 0

		for i in range(len(_voltageVector)-1):
			vMin = _voltageVector[i]
			vMax = _voltageVector[i+1]
			vMinIdx = i
			vMaxIdx = i + 1

			if voltage >= vMin and voltage <= vMax:
				break

		pMin = _percentVector[vMinIdx]
		pMax = _percentVector[vMaxIdx]

		p = ( ( (voltage - vMin) * (pMax - pMin) ) / (vMax - vMin)) + pMin

	_lastPercentValues = _lastPercentValues[1:]
	_lastPercentValues.append(p)

	p = 0

	for i in range(_averageWindow):
		p += _lastPercentValues[i]

	p /= _averageWindow

	return int(p)
	
	#  (v -   vmin)  = (p - pMin)
	#  (vmax - vmin)   (pMax - pMin)
	#

	# (v - vmin) * (pMax - pMin) = (p - pMin) * (vmax - vmin)
	# (p - pMin) = ( (v - vmin) * (pMax - pMin) ) / (vmax - vmin)
	# p = ( ( (v - vmin) * (pMax - pMin) ) / (vmax - vmin)) + pMin

	# 3.3V  =  0%
	# 3.5V  =  3%
	# 3.6V  =  5%
	# 3.7V  =  8%
	# 3.8V  = 36%
	# 3.9V  = 62%
	# 4.0V  = 73%
	# 4.05V = 83%
	# 4.10V = 89%
	# 4.15V = 94%
	# 4.20V = 100%
