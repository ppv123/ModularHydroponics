import actuating
import sensing

import time


class PotData:
    nowData = {'lux': 0, 'waterLv': 0.0, 'ph': 0.0, 'temp': 0.0, 'hum': 0.0}
    wantData = {'lux': 0, 'waterLv': 0.0, 'ph': 0.0, 'temp': 0.0, 'hum': 0.0}


    def initKit(self):
        print("lux want: ")
        self.wantData['lux'] = int(input())

        print("waterLv want: ")
        self.wantData['waterLv'] = float(input())

        print("ph want: ")
        self.wantData['ph'] = float(input())

        print("temp want: ")
        self.wantData['temp'] = float(input())

        print("hum want: ")
        self.wantData['hum'] = float(input())


    def dataSensing(self):
        f = open("./nowdata.txt", 'w')

        self.nowData['lux'] = sensing.getLux()
        self.nowData['waterLv'] = sensing.getWaterLv()
        self.nowData['ph'] = sensing.getPh()
        self.nowData['temp'] = sensing.getTemp()
        self.nowData['hum'] = sensing.getHum()

        data = "%d temp, %d hum, %d lux" %(sensing.getTemp(), sensing.getHum(), sensing.getLux())
        f.write(data)
        
        f.close()


    def moduleAct(self):
        if self.nowData['lux'] < self.wantData['lux']:
            actuating.led(self)

        if self.nowData['waterLv'] < self.wantData['waterLv']:
            actuating.buzzer(self)

        if self.nowData['ph'] < self.wantData['ph']:
            actuating.pump(self)


def main():
    pot = PotData()

    while True:
        pot.dataSensing()
        if pot.nowData != pot.wantData:
            pot.moduleAct()

        time.sleep(300)  # 5분 주기로 반복


main()
