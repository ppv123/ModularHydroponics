import smbus
import pandas as pd
import RPi.GPIO as GPIO
import dbtask
import lcddriver
import keypaddriver
import time


bus = smbus.SMBus(1)

display = lcddriver.lcd()
button = keypaddriver.keypad()


class ModuleControl(object):
    modulenest = {} # = {'0x04': ('0x10', 'ph','actuator',0x02,'linear',0x04), '0x08':...}
    targetData = {} # = {'0x09': 7, '0x57': 15}
    currentData = {}


    def __init__(self, busnum):
        self.bus = smbus.SMBus(busnum)
        self.df = pd.read_csv('moduledata.csv')
        self.index = list(self.df)
        #0address,1category,2type,3actu_run,4control_model,5get_actu_status,6sensor_run
        #db = dbtask.DBtask('../../mandellion5/mandellion5/db.sqlite3')


    def initmodule(self): #1
        self.modulenest = {}
        self.targetData = {}
        self.currentData = {}
        for addr in range(128):
            try:
                self.bus.write_byte(addr, 0)
                #addr = hex(addr)
                self.findmeta(addr)
            except:
                pass


    def findmeta(self, address): #2
        filt = (self.df['address'] == address)
        meta = self.df[filt]
        data = [list([y for y in x]) for x in meta.values]
        self.modulenest[address] = data[0]


    def settarget(self):
        for key in self.modulenest.keys():
            if self.modulenest[key][2] == 'sensor':
                display.lcd_clear()
                display.lcd_long_write(display, self.modulenest[key][1] + ' :', 1)
                count = self.counting()
                display.lcd_long_write(display, self.modulenest[key][1] + ' set', 1)
                display.lcd_long_write(display, str(count), 2)
                time.sleep(0.5)
                self.targetData[key] = count  


    def viewsensingdata(self):
        num = 0
        for key in self.modulenest.keys():
            if self.modulenest[key][2] == 'sensor' :
                display.lcd_clear()
                num = float(key)
                num = int(num)
                self.bus.write_byte(num, 0x02) # always 0x02
                self.currentData[key] = self.bus.read_byte(num)
                display.lcd_clear()
                display.lcd_long_write(display, str(self.modulenest[key][1]) + ' :', 1)
                display.lcd_long_write(display, str(self.currentData[key]), 2)
                time.sleep(1)


    def viewtargetdata(self):
        for key in self.modulenest.keys():
            if self.modulenest[key][2] == 'sensor' :
                display.lcd_clear()
                display.lcd_long_write(display, str(self.modulenest[key][1]) + ' :', 1)
                display.lcd_long_write(display, str(self.targetData[key]), 2)
                time.sleep(1)


    def actuatemod(self):
        num = 0
        for key in self.modulenest.keys():#{'0x10': ('0x10', 'ph','actuator',0x02,'linear',0x04)}
            for value in self.modulenest.values():
                if value[1] == self.modulenest[key][1] and value[0] != key and value[2] == 'actuator':
                    num = float(key)
                    num = int(num)
                    self.bus.write_byte(num, 0x02) # always 0x02


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


'''
nod = ModuleControl(1)
nod.initmodule()
num = 0

for key in nod.modulenest.keys():
    if nod.modulenest[key][2] == 'sensor' :
        display.lcd_clear()
        num = float(key)
        num = int(num)
        nod.bus.write_byte(num, 0x02) # always 0x02
        nod.currentData[key] = nod.bus.read_byte(num)
        display.lcd_clear()
        display.lcd_long_write(display, str(nod.modulenest[key][1]) + ' :', 1)
        display.lcd_long_write(display, str(nod.currentData[key]), 2)
        time.sleep(1)
'''
bus.write_byte(3, 2)
time.sleep(5)
#nod = ModuleControl(1)
#nod.initmodule()

#nod.bus.write_byte(3, 2)
#nod.actuatemod()
'''
for key in nod.modulenest.keys():
    print(nod.modulenest[key])
'''