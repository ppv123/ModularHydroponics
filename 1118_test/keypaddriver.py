import RPi.GPIO as GPIO
import lcddriver
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

display = lcddriver.lcd()



class keypad:
    def __init__(self):
        self.lcd_out=False

    def key_input(self):
        #try:
        while True:
            up_state = GPIO.input(18)
            select_state = GPIO.input(23)
            #down_state = GPIO.input(24)
            if not up_state:
                #display.lcd_clear()
                #display.lcd_long_write(display, "up", 1)
                time.sleep(0.2)
                return True
            elif not select_state:
                #display.lcd_clear()
                #display.lcd_long_write(display, "select", 1)
                time.sleep(0.2)
                return False
            #elif not down_state:
                #display.lcd_clear()
                #display.lcd_long_write(display, "down", 1)
                #time.sleep(0.2)
                #return True
            
            #if (not up_state) or (not select_state) or (not down_state):
            #if not (up_state and select_state and down_state):
                #display.lcd_clear()
                #display.lcd_long_write(display, "lcd_clear", 1)
                #time.sleep(1)
                #break
        #except KeyboardInterrupt:
            #break

#key = keypad()

#key.key_input()
    def key_count(self,display, name):
        '''
        count = 0
        while True:
            up_state = GPIO.input(18)
            select_state = GPIO.input(23)
            # down_state = GPIO.input(24)
            if not up_state:
                time.sleep(0.5)
                while True:
                    if not up_state:
                        time.sleep(0.2)
                        count += 1
                    if up_state:
                        time.sleep(0.2)
                        break
                return count
            elif not select_state:
                time.sleep(0.2)
                return False
        '''
        display.lcd_clear()
        display.lcd_long_write(display, name + ' : ', 1)
        count = 0
        while True:
            putB = key_input()
            if putB:
                time.sleep(0.5)
                count += 1
                display.lcd_long_write(display, str(count), 2)
                while True:
                    putB = key_input()
                    if putB:
                        time.sleep(0.2)
                        count += 1
                        display.lcd_long_write(display, str(count), 2)
                        #time.sleep(0.2)
                    elif not putB:
                        time.sleep(0.2)
                        break
                    
            #break
            return count
