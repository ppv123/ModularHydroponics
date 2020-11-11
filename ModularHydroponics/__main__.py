from ModularHydroponics import interface, menu, taskmanage, modulecontrol, gpiocontrol
import threading
import time
import random


def setup(**kwargs):
    gpiocontrol.gpio_setup()

    qsem = threading.Semaphore(1)
    autoconq = taskmanage.OperationQueue(1, qsem)
    senseconq = taskmanage.OperationQueue(1, qsem)
    modcon = modulecontrol.ModuleControl(1)

    #최상위
    mainMenu = menu.Menu("Main", 0)
    initmod = menu.ExecOption("Initialize Modules", 1, mainMenu, function=modcon.initmodule)
    controlMenu = menu.SubMenu("Control", 2, mainMenu)
    monMenu = menu.SubMenu("Monitoring", 3, mainMenu)

    #1.control
    setcontrol = menu.ExecOptionList("Module Control Mode", 1, controlMenu, funcdic=modcon.getmodulemode, mode=True,
                                     trueopt='Auto', falseopt='Manual')
    refreshq = menu.ExecOption("Refresh Auto Queue", 2, controlMenu, function=modcon.initautoQ, opq=autoconq)
    mancontrol = menu.ExecOptionList("Control Manually", 3, controlMenu, funcdic=modcon.getmodulemode, mode=False)
    targetval = menu.ExecOption("Set target value", 4, controlMenu, function=modcon.settarget)

    autocondic = {'run_async': True, 'infinite': True}
    autocontrol = menu.ToggleOption("control mode", 5, controlMenu, function=autoconq.start, function2=autoconq.stop,
                                    trueopt='Running', falseopt='Stopped', funcargs=autocondic)



    #2. monitoring
    sensorconfig = menu.SubMenu("Sensor Configuration", 1, monMenu)
    sensorstat = menu.ExecOption("Sensor Modules", 2, monMenu, function='')
    actustat = menu.ExecOption("Actuator Modules", 3, monMenu, function='')

    return mainMenu



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
