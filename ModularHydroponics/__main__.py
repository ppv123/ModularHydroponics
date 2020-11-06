from ModularHydroponics.ModularHydroponics import interface, menu, taskmanage#, modulecontrol
import time
import random


def menu_setup(**kwargs):
    q = kwargs.pop('q')
    n = kwargs.pop('n')
    para1 = kwargs.pop('para1')

    #최상위
    mainMenu = menu.Menu("Main", 0)
    controlMenu = menu.SubMenu("Control", 1, mainMenu)  #1
    monMenu = menu.SubMenu("Monitoring", 2, mainMenu)   #2
    #moduleMenu = menu.SubMenu("Module Status", 3, mainMenu) #3

    #1.control
    targetval = menu.ExecOption("Set target value", 1, controlMenu, function=testfunction, para1=para1)
    mancontrol = menu.SubMenu("Control Manually", 2, controlMenu)
    autocontrol = menu.ToggleOption("control mode", 3, controlMenu, function=startq, function2=stopq,
                                    opq=q, trueopt='Running', falseopt='Stopped')

    #2. monitoring
    sensorstat = menu.ExecOption("Sensor Modules", 1, monMenu, function='')
    actustat = menu.ExecOption("Actuator Modules", 2, monMenu, function='')

    return mainMenu


def testfunction(**kwargs):
    para1 = kwargs.pop('para1', 'didnt get any kwargs')
    print("execute success", para1)


def somei2c_operation(**kwargs):
    n = kwargs.pop('n', 4)
    for i in range(n):
        print(i, end='')
        time.sleep(0.25)


def startq(**kwargs):
    opq = kwargs['opq']
    opq.start(True)


def stopq(**kwargs):
    opq = kwargs['opq']
    opq.stop()


autoconq = taskmanage.OperationQueue(1)
interface.cmd_line(menu_setup, q=autoconq, para1='just for test', n=15)


'''
    1.control
        1) target value
        2) auto/manual
        3) manual mode scheduling
    2.monitoring
        1) 
    3.module status
        -> show category(actuator / sensor), i2c address
    4.web status
'''
