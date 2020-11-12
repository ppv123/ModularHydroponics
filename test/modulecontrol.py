import smbus
import time
import pandas as pd
import RPi.GPIO as GPIO
import dbtask


class ModuleControl(object):
    targetData = {}
    modulenest = {}
    autocon = {}
    sensors = []
    currentdata = {}

    def __init__(self, busnum):
        self.bus = smbus.SMBus(busnum)
        self.df = pd.read_csv('moduledata.csv')
        self.index = list(self.df)
        #0address,1category,2type,3actu_run,4control_model,5get_actu_status,6sensor_run
        #db = dbtask.DBtask('../../mandellion5/mandellion5/db.sqlite3')

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

        for key in self.modulenest.keys():
            self.initautocon(key)
            self.initsensor(key)

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

    def initautocon(self, address):   #autocon에 존재-> 자동모드 가능,key: 주소, value: 해당 모듈자동모드 설정 여부
        for value in self.modulenest.values():
            if value[1] == self.modulenest[address][1] and value[0] != address:
                self.autocon[address] = False

    def initsensor(self, address):
        for value in self.modulenest.values():
            if value[1] == 'sensor':
                self.sensors.append(value[0])

    def settarget(self):
        if self.autocon:
            for key in self.autocon.keys():
                self.targetData[key] = input("category => Value: ".format(category=self.modulenest[key][1]))

    def toggleauto(self, **kwargs):
        address = kwargs.pop('address', None)
        try:
            self.autocon[address] = not self.autocon[address]
            return self.autocon[address]
        except:
            pass

    def initautoQ(self, **kwargs):
        opq = kwargs.pop('opq', None)
        try:
            opq.flush()
            for key, value in self.autocon:
                if value:
                    #find control model by address
                    #wrap actuate with control model, add wrapped function
                    opq.add(method='', address=key)
        except:
            pass

    def getmodulemode(self, **kwargs):
        mode = kwargs.pop('mode', False)
        dict = {}
        for index, (key, value) in enumerate(self.autocon.items()):
            if value is mode:
                dict[index] = (self.toggleauto, key, {'address': key})
            else:
                dict[index] = (self.actmodule_man, key, {'address': key})
        return dict

    def senseall(self, **kwargs):
        opq = kwargs.pop('opq', None)
        try:
            opq.flush()
            for i in range(len(self.sensors)):
                opq.add(self.actmodule_man, address=self.sensors[i])
        except:
            pass

    def actmodule_man(self, **kwargs):
        actusign = kwargs.pop('actusign')
        address = kwargs.pop('address')
        if self.isvalidmodule(address):
            if self.modulenest[address][2] == 'sensor':
                self.bus.write_byte(address, int(self.modulenest[address][6]))
                #+ time, logging, db insertion
                return self.bus.read_byte(address)
            elif self.modulenest[address][2] == 'actuator':
                if actusign:
                    self.bus.write_byte(address, int(self.modulenest[address][3])) # increasing(+) way
                    #return self.bus.read_byte(address) #actuator 실행하고 상태 반환받음 좋겠다.
                else:
                    self.bus.write_byte(address, int(self.modulenest[address][3])) #3 -> something else
        else:
            print('invalid module')