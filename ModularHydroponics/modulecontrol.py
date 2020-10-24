import smbus
import time
import subprocess
import RPi.GPIO as GPIO


class ModuleControl(object):
    def __init__(self, busnum):
        self.bus = smbus.SMBus(busnum)
        self.nowData = {}
        self.wantData = {}
        self.address = {}
        self.moduletype = {}
        self.instrQ = []

    def initi2c(self):
        for i in range(128):
            try:
                self.bus.write_byte(i, 0)
                self.address[i] = hex(i)
            except:
                pass

        # return self.address  # = {'lux': 0x04, 'tempHum': 0x08, 'ph': 0x10}
                                # = {'4': 0x04, '8': 0x08, '10': 0x10}
    def gettype(self):
        self.moduletype = self.address.copy()
        #print(self.module_type)
        for i in self.moduletype.keys():
            self.bus.write_byte(self.moduletype[i], 1) #arduino가 1을 받으면 타입 반환
            #self.module_type = 4
            typesent = self.bus.read_byte(self.moduletype[i])
            if typesent == 1:
                self.moduletype[self.moduletype[i]] = 'sensing'
            elif typesent == 2:
                self.moduletype[self.moduletype[i]] = 'actuating'
                self.bus.write_byte(self.moduletype[i], self.wantData[i])
        # sensor, actuator 분류에다 세부 type(ph, lux, temp..)도 필요
        #
        # return self.module_type

    def actall(self):
        for i in self.address.keys():
            self.bus.write_byte(self.address[i], 2) #arduino가 2를 받으면 모듈 작동(sensing or acting)
            checking = self.bus.read_byte(self.address[i])
            if checking != 0:   # not None
                self.nowData = checking

'''                
    def act(self, **kwargs):
        주소, 인덱스, 혹은 이름에 해당하는 모듈에 instruction code 전달
        
'''
#eventline 제어
#display 제어

def main(): #->스크립트화해서 셋업단계에서 실행
    #I2C 충돌 안 나게 큐에 넣어서 실행되게끔 하기
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    modcon1 = ModuleControl(1)
    while True:


        modcon1.initi2c()  # return self.address
        modcon1.gettype()  # return self.module_type
        modcon1.actall()   # return self.nowData or acting

        for i in modcon1.address.keys():
            print("%s %s" % (i, modcon1.address[i]))

        for i in modcon1.moduletype.keys():
            print("%s %s" % (i, modcon1.moduletype[i]))

        time.sleep(5)  # 5초 주기로 반복