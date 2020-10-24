import time
import board
import busio
import adafruit_am2320
import smbus

I2C_CH_1 = 1
CONT_H_RES_MODE = 0x10
BH1750_DEV_ADDR = 0x23

bus = smbus.SMBus(1)
address3 = 0x04

i2c2 = smbus.SMBus(I2C_CH_1)
i2c = busio.I2C(board.SCL, board.SDA)
am = adafruit_am2320.AM2320(i2c)


def getData(address):
    if address == 0x23:
        lux_bytes = i2c2.read_i2c_block_data(BH1750_DEV_ADDR, CONT_H_RES_MODE, 2)
        lux = int.from_bytes(lux_bytes, byteorder='big')
        return lux

    if address == 0x5c: # sensing_ver2 40~48라인에서 while 제거
        temp = 0
        hum = 0
        for i in range(0, 2):
            temp = am.temperature
            hum = am.relative_humidity

        return temp, hum

    if address == 0x38:
        ph = bus.read_byte(address3)
        ph = ph / 10

        return ph
