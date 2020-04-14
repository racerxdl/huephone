from machine import Pin, ADC
import time, ujson

from niceduration import *

IP5306_ADDR = 0x75

_batteryPin = ADC(Pin(35))
_batteryPin.atten(ADC.ATTN_11DB)
_batteryPin.width(ADC.WIDTH_12BIT)

_averageWindow = 20
_numAdcSamples = 4
_adcSleepTime = 0.001
_voltageVector = [3.3, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.05, 4.10, 4.15]
_percentVector = [  0,   3,   5,   8, 36,  62,  73,   83,   89,   100]
_lastPercentValues = [ 100 for x in range(_averageWindow) ]


def KeepBoostPowerOn(i2c):
  print("IP5306 Boost Power On")
  i2c.writeto_mem(IP5306_ADDR, 0x00, "\x37")

def IsBatteryFull(i2c):
	return True if i2c.readfrom_mem(IP5306_ADDR, 0x71, 1)[0] & 0b1000 > 0 else False

def IsChargingCableOn(i2c):
	return True if i2c.readfrom_mem(IP5306_ADDR, 0x70, 1)[0] & 0b1000 > 0 else False

def GetBatteryVoltage():
	val = 0
	for i in range(_numAdcSamples):
		val += _batteryPin.read()
		time.sleep(_adcSleepTime)

	val /= _numAdcSamples
	# 0 -> 3.6V
	# 0 -> 4096
	return 3.6 * ((val * 2) / 4096)

def GetBatteryPercent():
	global _lastPercentValues
	voltage = GetBatteryVoltage()

	if voltage <= 3.3:
		p = 0
	elif voltage >= 4.15:
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

_calibratePercentDelta = 5
_lastEstimatePercent = 100
_lastEstimateTime = time.time()
_percentsPerSecond = 0

def Calibrate():
	global _lastEstimatePercent
	global _percentsPerSecond
	global _lastEstimateTime
	currentPercent = GetBatteryPercent()

	if _lastEstimatePercent - currentPercent > _calibratePercentDelta:
		timeDelta = time.time() - _lastEstimateTime
		percentDelta = _lastEstimatePercent - currentPercent
		_lastEstimatePercent = currentPercent
		_lastEstimateTime = time.time()

		_percentsPerSecond = percentDelta / timeDelta
		SavePercentsPerSecond()


def SavePercentsPerSecond():
	global _percentsPerSecond
	currentPercent = GetBatteryPercent()
	data = {}
	try:
		f = open("calibrate.json", "r")
		f.seek(0)
		sdata = f.read()
		f.close()
		data = ujson.loads(sdata)
	except:
		pass

	data[currentPercent] = _percentsPerSecond

	f = open("calibrate.json", "w")
	f.write(ujson.dumps(data))
	f.close()

def EstimateBattery():
	global _percentsPerSecond
	
	if _percentsPerSecond == 0:
		return "Calculating"

	currentPercent = GetBatteryPercent()
	numSecondsToZero = currentPercent / _percentsPerSecond
	return SecondsToNiceDuration(numSecondsToZero)
