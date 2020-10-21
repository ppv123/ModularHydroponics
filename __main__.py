from ModularHydroponics import interface
from ModularHydroponics import menu
from ModularHydroponics import taskmanage
import time
import random

def menu_setup():
    mainMenu = menu.Menu("Main", 0)
    controlMenu = menu.SubMenu("Control", 1, mainMenu)
    monMenu = menu.SubMenu("Monitoring", 2, mainMenu)
    moduleMenu = menu.SubMenu("Module Status", 3, mainMenu)

    targetval = menu.ExecOption("Set target value", 1, controlMenu, testfunction, )
    autocontrol = menu.ToggleOption("control mode", 2, controlMenu, testfunction, 'Auto', 'Manual')

    return mainMenu


def testfunction(queue, method):
    print("execute success")


def somei2c_operation(n):
    for i in range(n):
        print(i)
        time.sleep(0.25)


i2cque = taskmanage.OperationQueue(1)
test = {'queue': i2cque, 'n': }

interface.cmd_line(menu_setup)