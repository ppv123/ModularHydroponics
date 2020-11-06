import smbus
import time
import pandas as pd
import RPi.GPIO as GPIO
import queue
from ModularHydroponics.ModularHydroponics import taskmanage


class ModuleControl(object):
    targetData = {}
    modulenest = {}
    autocon = {}

    def __init__(self, busnum):
        self.bus = smbus.SMBus(busnum)
        self.df = pd.read_csv('moduledata.csv')
        self.index = list(self.df)  #address,category,type,actu_run,control_model,get_actu_status,sensor_run
        self._reservQ = taskmanage.OperationQueue()

    def initmodule(self):
        for addr in range(128):
            self.bus.write_byte(addr, 0)
            try:
                self.findmeta(addr)

            except:
                print('unknown module')
                if input('Add unknow module? Y/N') == 'Y':
                    meta = (addr, 'unknown', None, None, None, None)
                    self.modulenest[addr] = meta

    def findmeta(self, address):
        filt = (self.df['address'] == address)
        meta = self.df[filt]
        data = [tuple([y for y in x]) for x in meta.values]
        self.modulenest[address] = data

    def isvalidmodule(self, address):
        try:
            self.bus.write_byte(address, 0)
            return True

        except:
            self.modulenest.pop(address)
            return False

    def isautonow(self, address):
        return self.autocon[address]

    def isautocon(self, address):   #자동모드 가능?
        for value in self.modulenest.values():
            if value[1] == self.modulenest[address][1] and value[0] != address:
                for addr in self.autocon:
                    if addr == address:
                        return True
                self.autocon[address] = False
                return True
        self.autocon.pop(address)
        return False

    def settarget(self):
        for key, value in self.autocon:
            self.targetData[key] = input("category => Value: ".format(category=self.modulenest[key][1]))

    def toggleauto(self, address):
        self.autocon[address] = not self.autocon[address]

    def setautoQ(self):
        self._reservQ.flush()
        for key, value in self.autocon:
            if value:
                self._reservQ.add(method=self.actmodule_man, address=key)
        return self._reservQ

    def actmodule_man(self, **kwargs):
        address = kwargs.pop('address')
        if self.isvalidmodule(address):
            if self.modulenest[address][2] == 'sensor':
                self.bus.write_byte(address, int(self.modulenest[address][6]))
                return self.bus.read_byte(address)
            elif self.modulenest[address][2] == 'actuator':
                self.bus.write_byte(address, int(self.modulenest[address][3]))
                #return self.bus.read_byte(address) #actuator 실행하고 상태 반환받음 좋겠다.
        else:
            print('invalid module')






#eventline 제어
#display 제어

def main(): #->스크립트화해서 셋업단계에서 실행
    #I2C 충돌 안 나게 큐에 넣어서 실행되게끔 하기
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    modcon1 = ModuleControl(1)
    while True:


        modcon1.initi2c()  # return self.address

        modcon1.actall()   # return self.nowData or acting

        for i in modcon1.address.keys():
            print("%s %s" % (i, modcon1.address[i]))

        for i in modcon1.moduletype.keys():
            print("%s %s" % (i, modcon1.moduletype[i]))

        time.sleep(5)  # 5초 주기로 반복

