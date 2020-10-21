import smbus
from ModularHydroponics.ver3.i2cInit import i2cInit


def check():
    checking = {}

    i2cInit()

    for i in range(0, 2):
        for device in range(128):
            try:
                bus.write_byte(device, 0)
                if hex(device) == "0x23":

                if:
                    pass

            except():
                pass

    return checking
