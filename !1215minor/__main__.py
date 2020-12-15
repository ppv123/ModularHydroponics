import interface, menu, taskmanage, modulecontrol, gpiocontrol
import threading
import time
import random
#from multiprocessing import Process

modcon = modulecontrol.ModuleControl(1) #up from line17


def setup(**kwargs):
    gpiocontrol.gpio_setup()

    qsem = threading.Semaphore(1)
    autoconq = taskmanage.OperationQueue(1, qsem=qsem)
    senseconq = taskmanage.OperationQueue(1, qsem=qsem)

    #0. main
    mainMenu = menu.Menu("Main", 0)
    initmod = menu.ExecOption("Init Module", 1, mainMenu, function=modcon.initmodule)
    controlMenu = menu.SubMenu("Control", 2, mainMenu)
    monMenu = menu.SubMenu("Monitoring", 3, mainMenu)

    #1.control
    targetval = menu.ExecOption("Set target", 1, controlMenu, function=modcon.settarget)
    actuating = menu.ExecOption("Actuating", 2, controlMenu, function=modcon.actuatemod)
    
    #2. monitoring
    sensorstat = menu.ExecOption("Sensor", 1, monMenu, function=modcon.viewsensingdata)
    targetstat = menu.ExecOption("Target", 2, monMenu, function=modcon.viewtargetdata)

    return mainMenu


interface.cmd_line(setup, para1 = 'just for test', n=15)


#Process(target=interface.cmd_line, args=(setup,)).start()
#Process(target=modcon.controlmod).start()