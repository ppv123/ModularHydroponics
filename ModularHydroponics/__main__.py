from ModularHydroponics import interface, menu, taskmanage, modulecontrol, gpiocontrol
import time
import random


def setup(**kwargs):
    q = kwargs.pop('q')
    n = kwargs.pop('n')
    para1 = kwargs.pop('para1')
    gpiocontrol.gpio_setup()

    autoconq = taskmanage.OperationQueue(1)
    senseconq = taskmanage.OperationQueue(1)
    modcon = modulecontrol.ModuleControl(1)

    #최상위
    mainMenu = menu.Menu("Main", 0)
    initmod = menu.ExecOption("Initialize Modules", 1, mainMenu, function=modcon.initmodule)
    controlMenu = menu.SubMenu("Control", 2, mainMenu)  #1
    monMenu = menu.SubMenu("Monitoring", 3, mainMenu)   #2

    #1.control
    setcontrol = menu.ExecOptionList("Module Control Mode", 1, controlMenu, funcdic=modcon.getautomoddict(),
                                     trueopt='Auto', falseopt='Manual', )
    targetval = menu.ExecOption("Set target value", 2, controlMenu, function=modcon.settarget)
    mancontrol = menu.ExecOptionList("Control Manually", 3, controlMenu)

    autocondic = {'run_async': True, 'infinite': True}
    autocontrol = menu.ToggleOption("control mode", 4, controlMenu, function=autoconq.start, function2=autoconq.stop,
                                    trueopt='Running', falseopt='Stopped', funcargs=autocondic)



    #2. monitoring
    sensorconfig = menu.SubMenu("Sensor Configuration", 1, monMenu)
    sensorstat = menu.ExecOption("Sensor Modules", 2, monMenu, function='')
    actustat = menu.ExecOption("Actuator Modules", 3, monMenu, function='')

    return mainMenu


def testfunction(**kwargs):
    para1 = kwargs.pop('para1', 'didnt get any kwargs')
    print("execute success", para1)


def somei2c_operation(**kwargs):
    n = kwargs.pop('n', 4)
    for i in range(n):
        print(i, end='')
        time.sleep(0.25)

'''
def startq(**kwargs):
    opq = kwargs['opq']
    opq.start(True)


def stopq(**kwargs):
    opq = kwargs['opq']
    opq.stop()
'''


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
