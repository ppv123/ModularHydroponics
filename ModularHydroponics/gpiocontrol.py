import GPIO
import subprocess

def restart(): #Raspberry Pi 재부팅 코드
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)


def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.add_event_detect(16, GPIO.FALLING, callback=restart, bouncetime=1000)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
