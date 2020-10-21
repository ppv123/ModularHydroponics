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
        for j in range(128):
            try:
                bus.write_byte(j, 0)
                self.address[j] = hex(j)
                print(j)
            except:
                pass

        # return self.address  # = {'lux': 0x04, 'tempHum': 0x08, 'ph': 0x10}

    def getType(self):
        self.module_type = self.address.copy()
        print(self.module_type)
        for j in self.module_type.keys():
            bus.write_byte(self.module_type, 1)
            # self.module_type = 4
            type_send = bus.read_byte(4)
            if type_send == 1:
                self.module_type[4] = 'sensing'
            elif type_send == 2:
                self.module_type[4] = 'actuating'

        # return self.module_type


def main():
    pot = PotData()
    while True:
        pot.initI2C()  # return self.address
        pot.getType()  # return self.module_type

        for i in pot.address.keys():
            print("%s %s" % (i, pot.address[i]))

        for i in pot.module_type.keys():
            print("%s %s" % (i, pot.module_type[i]))

        time.sleep(5)  # 5초 주기로 반복


main()
