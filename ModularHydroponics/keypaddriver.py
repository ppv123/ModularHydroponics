import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class keypad:
    def key_input(self):
        while True:
            up_state = GPIO.input(18)
            select_state = GPIO.input(23)
            down_state = GPIO.input(24)
            if not up_state:
                return 1
            elif not select_state:
                return 0
            elif not down_state:
                return -1
