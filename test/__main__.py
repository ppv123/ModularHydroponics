import interface, menu, taskmanage, modulecontrol, gpiocontrol
import threading
import time
import random


def setup(**kwargs):
    gpiocontrol.gpio_setup()

    qsem = threading.Semaphore(1)
    autoconq = taskmanage.OperationQueue(1, qsem=qsem)
    senseconq = taskmanage.OperationQueue(1, qsem=qsem)
    modcon = modulecontrol.ModuleControl(1)

    mainMenu = menu.Menu("Main", 0)
    initmod = menu.ExecOption("Initialize Module", 1, mainMenu, function=modcon.initmodule)
    controlMenu = menu.SubMenu("Control", 2, mainMenu)
    monMenu = menu.SubMenu("Monitoring", 3, mainMenu)

    #1.control
    '''
    setcontrol = menu.ExecOptionList("Module Control Mode", 1, controlMenu, funcdic=modcon.getmodulemode, mode=True,
                                     trueopt='Auto', falseopt='Manual')
    refreshq = menu.ExecOption("Refresh Auto Queue", 2, controlMenu, function=modcon.initautoQ, opq=autoconq)
    mancontrol = menu.ExecOptionList("Control Manually", 3, controlMenu, funcdic=modcon.getmodulemode, mode=False)
    '''
    #==
    funcdic1 = modcon.getmodulemode(mode = True)
    setcontrol = menu.ExecOptionList("Module Control Mode", 1, controlMenu, funcdic=funcdic1, mode=True,
                                     trueopt='Auto', falseopt='Manual')
    refreshq = menu.ExecOption("Refresh Auto Queue", 2, controlMenu, function=modcon.initautoQ, opq=autoconq)
    funcdic2 = modcon.getmodulemode(mode = False)
    mancontrol = menu.ExecOptionList("Control Manually", 3, controlMenu, funcdic=funcdic2)
    #==
    
    targetval = menu.ExecOption("Set target value", 4, controlMenu, function=modcon.settarget)

    autocondic = {'run_async': True, 'infinite': True}
    autocontrol = menu.ToggleOption("control mode", 5, controlMenu, function=autoconq.start, function2=autoconq.stop,
                                    trueopt='Running', falseopt='Stopped', funcargs=autocondic)



    #2. monitoring
    sensorconfig = menu.SubMenu("Sensor Configuration", 1, monMenu)
    sensorstat = menu.ExecOption("Sensor Modules", 2, monMenu, function='')
    actustat = menu.ExecOption("Actuator Modules", 3, monMenu, function='')

    return mainMenu



interface.cmd_line(setup, para1 = 'just for test', n=15)


