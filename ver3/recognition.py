import smbus


def check():
    checking = {}

    bus_number = 1
    bus = smbus.SMBus(bus_number)

    for i in range(0, 2):
        for device in range(128):
            try:
                bus.write_byte(device, 0)
                if hex(device) == "0x23":
                    checking['lux'] = 0x23

                if hex(device) == "0x5c":
                    checking['tempHum'] = 0x5c

                if hex(device) == "0x38":
                    checking['ph'] = 0x38

            except():
                pass

    return checking
