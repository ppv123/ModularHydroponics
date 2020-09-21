import actuating
import sensing

import time

nowdata = {'lux':0, 'ph':0.0, 'temp':0.0, 'hum' : 0.0}
wantdata = {'lux':0, 'ph':0.0, 'temp':0.0, 'hum' : 0.0}


def initKit():

    print("lux want: ")
    wantdata['lux'] = int(input())

    print("waterLv want: ")
    wantdata['waterLv'] = float(input())

    print("ph want: ")
    wantdata['ph'] = float(input())

    print("temp want: ")
    wantdata['temp'] = float(input())

    print("hum want: ")
    wantdata['hum'] = float(input())


def dataUpdate():
    global nowdata
    i = 0
    f = open("./nowdata.txt", 'w')

    nowdata['lux'] = sensing.getLux()
    nowdata['waterLv'] = sensing.getWaterLv()
    nowdata['ph'] = sensing.getPh()
    nowdata['temp'] = sensing.getTemp()
    nowdata['hum'] = sensing.getHum()


    while (i < numModule):
        f.write("%f\n" %nowdata[i])
        i += 1

    f.close()

def moduleAct():

    if(nowdata['lux'] < wantdata['lux']):
        actuating.led()

    if(nowdata['waterLv'] < wantdata['waterLv']):
        actuating.buzzer()

    if(nowdata['ph'] < wantdata['ph']):
        actuating.valve()


def main():
    global nowdata
    global wantdata

    while(True):
        dataUpdate()
        if (nowdata != wantdata):
            moduleAct()
        time.sleep(300)  #5분 주기로 반복

main()