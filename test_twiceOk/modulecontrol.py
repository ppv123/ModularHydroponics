import smbus
import time
import pandas as pd
import RPi.GPIO as GPIO
import dbtask
import lcddriver
import keypaddriver

display = lcddriver.lcd()
button = keypaddriver.keypad()

class ModuleControl(object):
    modulenest = {}#'0x10': ('0x10', 'ph','actuator',0x02,'linear',0x04)}
    autocon = {}#{'0x10': True}
    sensors = []
    targetData = {}

    def __init__(self, busnum):
        self.bus = smbus.SMBus(busnum)
        self.df = pd.read_csv('moduledata.csv')
        self.index = list(self.df)
        #0address,1category,2type,3actu_run,4control_model,5get_actu_status,6sensor_run
        #db = dbtask.DBtask('../../mandellion5/mandellion5/db.sqlite3')

    def initmodule(self):
        '''
        for addr in range(128):
            self.bus.write_byte(addr, 0)
            try:
                self.findmeta(addr)#(addr)

            except:
                print('unknown module')
                if input('Add unknow module? Y/N') == 'Y':
                    meta = (addr, 'unknown', None, None, None, None)
                    self.modulenest.setdefault(addr)
                    self.modulenest[addr] = meta
'''
        self.findmeta('0x01')
        self.findmeta('0x02')
        self.findmeta('0x03')
        self.findmeta('0x04')
        self.findmeta('0x05')
        self.findmeta('0x06')
        self.findmeta('0x07')
        
        for key in self.modulenest.keys():
            self.initautocon(key)
            self.initsensor(key)

    def findmeta(self, address):
        filt = (self.df['address'] == address)
        meta = self.df[filt]
        data = [tuple([y for y in x]) for x in meta.values]
        #data.remove(str(address))
        #print(data)
        #self.modulenest.setdefault(str(address), data)
        self.modulenest[address] = data[0]

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
        for value in self.modulenest.values():#{'0x10': ('0x10', 'ph','actuator',0x02,'linear',0x04)}
            if value[1] == self.modulenest[address][1] and value[0] != address and value[2] == 'actuator':
                self.autocon[address] = False
                #return

    def initsensor(self, address):
        for value in self.modulenest.values():
            if value[1] == 'sensor':
                self.sensors.append(value[0])


            #adr=[]
            #for key in self.autocon.keys():#address str
            #    if self.autocon[key]: # True True
            #        adr.append(key)  
            #for key in adr:
            
    def settarget(self):
        #if self.autocon: # always True
        for key in self.autocon.keys():
            if self.autocon[key] != True :
                print(self.modulenest[key][1], end='')
                display.lcd_clear()
                display.lcd_long_write(display, self.modulenest[key][1] + ' : ', 1)
                count = 0
                display.lcd_long_write(display, str(count), 2)
                while True:
                    putB = button.key_input()
                    if putB:
                        time.sleep(0.1)
                        count += 1
                        display.lcd_long_write(display, str(count), 2)
                        while True:
                            putB = button.key_input()
                            if putB:
                                time.sleep(0.001)
                                count += 1
                                display.lcd_long_write(display, str(count), 2)
                            elif not putB:
                                time.sleep(0.001)
                                break 
                    break
                display.lcd_long_write(display, ' want ' + self.modulenest[key][1] + ' is', 1)
                display.lcd_long_write(display, str(count), 2)
                time.sleep(1)
                self.targetData[key] = count
                ##
            
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
                dict[index] = (self.toggleauto(address=key), key, {'address': key})
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
            



nod = ModuleControl(1)
nod.initmodule()
print(nod.autocon)
nod.getmodulemode(mode = False)
print(nod.autocon)
print(nod.targetData)

'''
print(bool(nod.autocon))
adr=[]
for key in nod.autocon.keys():#address str
    if nod.autocon[key]: # True True
        adr.append(key)
print(adr)

for i in adr:
    print('a')
nod.settarget()


if nod.autocon:
            for key, value in nod.autocon.items():
                #if not value:
                if value != True:
'''
'''
modulenest = {'0x08': ('0x08', 'ph','sensor',None,None,None, 0x02),
              '0x10': ('0x10', 'ph','actuator',0x02,'linear',0x04, None),
              '0x06': ('0x06', 'wq','sensor',None,None,None, 0x02),
              '0x04': ('0x04', 'led','actuator',0x02,'linear',0x04, None),
              '0x12': ('0x12', 'led','sensor',None,None,None, 0x02)}


autocon = {}

def test(modulenest):
    for key in modulenest.keys():
        print(key)
        for value in modulenest.values():#{'0x10': ('0x10', 'ph','actuator',0x02,'linear',0x04)}
            print(value[1] + modulenest[key][1] + ' ' + value[0] + key)
            if value[1] == modulenest[key][1] and value[0] != key and value[2] == 'actuator':
                autocon[key] = False
                


test(modulenest)

print(autocon)
'''

'''
targetData = {}
'''


if nod.autocon:
    for key in nod.autocon.keys():
        nod.targetData[key] = input("category => Value: ".format(category=nod.modulenest[key][1]))


print(nod.targetData)
print(nod.autocon)

'''
modcon = ModuleControl(1)
modcon.autocon = autocon
#mode = kwargs.pop('mode', False)
dit = {}
for index, (key, value) in enumerate(autocon.items()):
    if value is False:
        dit[index] = (modcon.toggleauto(address=key), key, {'address': key})
    #else:
        #dit[index] = (modcon.actmodule_man(), key, {'address': key})

print(dit)
print(autocon)
'''