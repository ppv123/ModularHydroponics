import smbus
import time
#from time import sleep
import pandas as pd
import RPi.GPIO as GPIO
import dbtask
import lcddriver
import keypaddriver
import time

display = lcddriver.lcd()
button = keypaddriver.keypad()

class ModuleControl(object):
    modulenest = {}# = {'0x10': ('0x10', 'ph','actuator',0x02,'linear',0x04)}
    autocon = {}#{'0x10': True}
    sensors = []
    targetData = {}#{'0x09': 7, '0x57': 15}
    currentData = {}
    sensorfq = None
    
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

    def initautocon(self, address):
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
    
    def counting(self):
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
            return count
    
    def settarget(self):
        #if self.autocon: # always True
        for key in self.autocon.keys():
            if self.autocon[key] != True :
                print(self.modulenest[key][1], end='')
                display.lcd_clear()
                display.lcd_long_write(display, self.modulenest[key][1] + ' select :', 1)
                count = self.counting()
                display.lcd_long_write(display, self.modulenest[key][1] + ' set complete', 1)
                display.lcd_long_write(display, str(count), 2)
                time.sleep(1)
                self.targetData[key] = count
            
    def toggleauto(self, **kwargs):
        address = kwargs.pop('address', None)
        try:
            self.autocon[address] = not self.autocon[address]
            return self.autocon[address]
        except:
            print('toggleauto err')
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
                    #return self.bus.read_byte(address)
                else:
                    self.bus.write_byte(address, int(self.modulenest[address][3])) #3 -> something else
        else:
            print('invalid module')

    def checkvalue(self):
        display.lcd_clear()
        #display.lcd_long_write(display, str(self.autocon), 1)
        display.lcd_long_write(display, str(self.autocon), 1)
        display.lcd_long_write(display, str(self.targetData), 2)
        time.sleep(3)
        
        
    def initfrequency(self):
        display.lcd_clear()
        display.lcd_long_write(display, 'frequency setting', 1)
        time.sleep(1)
        self.sensorfq = self.counting()
        display.lcd_clear()
        display.lcd_long_write(display, 'frequency :', 1)
        display.lcd_long_write(display, str(self.sensorfq), 2)
        time.sleep(1)
            
    def viewsensingdata(self):
        while True:
            for key in self.modulenest.keys():
                self.currentdata[key] = self.actmodule_man(actusign=None, address=key)
                display.lcd_clear()
                display.lcd_long_write(display, self.modulenest[key][1] + ' :', 1)
                display.lcd_long_write(display, str(self.currentdata[key]), 2)
                putB = button.key_input()
                time.sleep(2)
            if not putB:
                    break
        '''
        display.lcd_clear()
        display.lcd_long_write(display, 'abc', 1)
        time.sleep(1)
        display.lcd_long_write(display, 'def', 1)
        putB = button.key_input()
        if not putB:
            break
        '''
        
    def viewactingdata(self):
        for key in self.modulenest.keys():
            display.lcd_clear()
            display.lcd_long_write(display, str(self.modulenest[key][1]) , 1)
            display.lcd_long_write(display, str(self.autocon[key]), 2)
            display.lcd_delay(2)
            #time.sleep(3)
            
    def settarget(self):
        #if self.autocon: # always True
        for key in self.autocon.keys():
            if self.autocon[key] != True :
                print(self.modulenest[key][1], end='')
                display.lcd_clear()
                display.lcd_long_write(display, self.modulenest[key][1] + ' select :', 1)
                count = self.counting()
                display.lcd_long_write(display, self.modulenest[key][1] + ' set complete', 1)
                display.lcd_long_write(display, str(count), 2)
                time.sleep(1)
                self.targetData[key] = count
            
'''
nod = ModuleControl(1)
nod.initmodule()
print(nod.autocon)
nod.getmodulemode(mode = False)
print(nod.autocon)
print(nod.targetData)
'''
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


#if nod.autocon:
 #   for key in nod.autocon.keys():
 #       nod.targetData[key] = input("category => Value: ".format(category=nod.modulenest[key][1]))


#print(nod.targetData)
#print(nod.autocon)


modcon = ModuleControl(1)
modcon.autocon = {'0x02': False, '0x03': False}
#mode = kwargs.pop('mode', False)
dit = {}
for index, (key, value) in enumerate(modcon.autocon.items()):
    if value is False:
        dit[index] = (modcon.toggleauto(address=key), key, {'address': key})
    #else:
        #dit[index] = (modcon.actmodule_man(), key, {'address': key})

print(dit)
print(modcon.autocon)
