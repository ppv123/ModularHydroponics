import time
import board
import busio
import adafruit_am2320
import smbus

I2C_CH_1 = 1

BH1750_DEV_ADDR = 0x23

CONT_H_RES_MODE = 0x10
CONT_H_RES_MODE2 = 0x11
CONT_L_RES_MODE = 0x13
ONETIME_H_RES_MODE = 0x20
ONETIME_H_RES_MODE2 = 0x21
ONETIME_L_RES_MODE = 0x23

i2c = smbus.SMBus(I2C_CH)   # pcf8574 io expansion board 제품 확인

i2c = busio.I2C(board.SCL, board.SDA)
am = adafruit_am2320.AM2320(i2c)


def getLux():
	lux = int.from_bytes(luxBytes, byteorder=’big’)
	return lux


def getPh():
	#아날로그 데이터를 뽑아오는 코드 연구 중
	return ph

def getWaterLv():
	#아날로그 데이터를 뽑아오는 코드 연구 중
	return waterLv


def getTemp():
	while True:
		for i in range(0, 2):
			try:
				temp = am.temperature
			except:
				pass
		time.sleep(2)
	return temp


def getHum():
	while True:
		for i in range(0, 2):
			try:
				hum = am.relative_humidity
			except:
				pass
	time.sleep(2)
	return hum