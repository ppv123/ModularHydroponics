import smbus

def i2cInit():
    I2C_CH_1 = 1
    bus = smbus.SMBus(1)

    CONT_H_RES_MODE = 0x10
    BH1750_DEV_ADDR = 0x23


    address3 = 0x04

    i2c2 = smbus.SMBus(I2C_CH_1)
    i2c = busio.I2C(board.SCL, board.SDA)
    am = adafruit_am2320.AM2320(i2c)