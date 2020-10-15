import smbus
import time

bus_number = 1
bus = smbus.SMBus(bus_number)


class PotData:
    nowData = {}

    # wantDate = {}

    def __init__(self):
        self.address = {}
        self.module_type = {}

    def initI2C(self):
        for i in range(0, 2):
            for j in range(128):
                try:
                    bus.write_byte(j, 0)
                    self.address[j] = hex(j)
                except():
                    pass
        return self.address  # = {'lux': 0x04, 'tempHum': 0x08, 'ph': 0x10}

    def getType(self, address):
        self.module_type = self.address.copy()

        for i in address:
            self.module_type = i
            type_send = bus.read_byte(address[i])

            if type_send == 1:
                self.module_type[i] = 'sensing'
            if type_send == 2:
                self.module_type[i] = 'actuating'

        return self.module_type


def main():
    while True:
        pot = PotData()
        pot.initI2C()  # return self.address
        pot.getType(pot.address)  # return self.module_type

        for i in pot.address.keys():
            print("%s %s" % (i, pot.address[i]))

        for i in pot.module_type.keys():
            print("%s %s" % (i, pot.module_type[i]))

        time.sleep(5)  # 5초 주기로 반복


main()
