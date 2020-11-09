from ModularHydroponics import interface, menu, taskmanage, modulecontrol
import time
import random


def setup(**kwargs):
    q = kwargs.pop('q')
    n = kwargs.pop('n')
    para1 = kwargs.pop('para1')
    autoconq = taskmanage.OperationQueue(1)
    modcon = modulecontrol.ModuleControl(1)

    #최상위
    mainMenu = menu.Menu("Main", 0)
    initmod = menu.ExecOption("Initialize Modules", 1, mainMenu, function=modcon.initmodule)
    controlMenu = menu.SubMenu("Control", 2, mainMenu)  #1
    monMenu = menu.SubMenu("Monitoring", 3, mainMenu)   #2

    #1.control
    targetval = menu.ExecOption("Set target value", 1, controlMenu, function=testfunction, para1=para1)
    mancontrol = menu.SubMenu("Control Manually", 2, controlMenu)
    autocontrol = menu.ToggleOption("control mode", 3, controlMenu, function=startq, function2=stopq,
                                    opq=q, trueopt='Running', falseopt='Stopped')
    setcontrol = menu.SubMenu("Control Manually", 4, controlMenu)

    sensorstat = menu.ExecOption("Sensor Modules", 1, monMenu, function='')

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



interface.cmd_line(setup, para1='just for test', n=15)


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
