import smbus
import time
import subprocess
import RPi.GPIO as GPIO

bus_number = 1
bus = smbus.SMBus(bus_number)


class PotData:
    def __init__(self):
        self.nowData = {}
        self.wantData = {}
        self.address = {}
        self.module_type = {}
        self.instrQ = []

    def initI2C(self):
        for j in range(128):
            try:
                bus.write_byte(j, 0)
                self.address[j] = hex(j)
            except:
                pass

        # return self.address  # = {'lux': 0x04, 'tempHum': 0x08, 'ph': 0x10}
                                # = {'4': 0x04, '8': 0x08, '10': 0x10}
    def getType(self):
        self.module_type = self.address.copy()
        #print(self.module_type)
        for i in self.module_type.keys():
            bus.write_byte(self.module_type[i], 1) #arduino가 1을 받으면 타입 반환
            #self.module_type = 4
            type_send = bus.read_byte(self.module_type[i])
            if type_send == 1:
                self.module_type[self.module_type[i]] = 'sensing'
            elif type_send == 2:
                self.module_type[self.module_type[i]] = 'actuating'
                bus.write_byte(self.module_type[i], self.wantData[i])

        # return self.module_type

    def action(self):
        for i in self.address.keys():
            bus.write_byte(self.address[i], 2) #arduino가 2를 받으면 모듈 작동(sensing or acting)
            checking = bus.read_byte(self.address[i])
            if checking != 0:   # not None
                self.nowData = checking


def restart(): #Raspberry Pi 재부팅 코드
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


def main():
    #I2C 충돌 안 나게 큐에 넣어서 실행되게끔 하기
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    pot = PotData()
    while True:
        GPIO.add_event_detect(3, GPIO.FALLING, callback=restart, bouncetime=1000)

        pot.initI2C()  # return self.address
        pot.getType()  # return self.module_type
        pot.action()   # return self.nowData or acting

        for i in pot.address.keys():
            print("%s %s" % (i, pot.address[i]))

        for i in pot.module_type.keys():
            print("%s %s" % (i, pot.module_type[i]))

        time.sleep(5)  # 5초 주기로 반복


main()
