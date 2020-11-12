import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class keypad:
    def key_input(self):
        while True:
            up_state = GPIO.input(18)
            select_state = GPIO.input(23)
            if not up_state:
                time.sleep(0.2)
                return True
            elif not select_state:
                time.sleep(0.2)
                return False

    def key_count(self):
        try:
            count = 0
            while True:
                putB = button.key_input()
                if putB:
                    time.sleep(0.5)
                    while True:
                        putB = button.key_input()
                        if putB:
                            time.sleep(0.1)
                            count += 1
                            #display.lcd_long_write(display, str(count), 1)
                        if not putB:
                            time.sleep(0.1)
                            #display.lcd_long_write(display, 'count: ' + str(count), 2)
                            break
                break

        except Keyboardinterrupt:
            #display.lcd_long_write(display, '-cleaning up- ', 1)
            #display.lcd_clear()
            sys.exit(1)
