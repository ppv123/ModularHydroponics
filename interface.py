import sys
import os
import threading
from . import menu



def cmd_line():
    currentmenu = menuSetup()
    currentmenu.run()
    while True:
        os.system('cls')
        cmd = input('\nSelect> ')
        try:
            currentmenu = handleoption(cmd, currentmenu)

        except KeyboardInterrupt:
            sys.exit(1)
            pass

def handleoption(cmd, menu):
    if cmd.isdecimal() and int(cmd) > 0:
        try:
            if isinstance(menu.subMenuObj[int(cmd)-1], ExecOption) or isinstance(menu.subMenuObj[int(cmd)-1], ToggleOption):
                menu.subMenuObj[int(cmd) - 1].run()
                menu.run()
                return menu
            else:
                menu.subMenuObj[int(cmd) - 1].run()
                return menu.subMenuObj[int(cmd) - 1]
        except:
            print('invalid submenu')
            return menu

    elif cmd.isdecimal() and int(cmd) == 0:
        if not menu.is_top():
            print('back to prevmenu')
            menu.prevMenu.run()
            return menu.prevMenu
        else:
            while True:
                ans = input('Quit program? Y/N>> ')
                for words in ['N', 'n', 'Y', 'y']:
                    if ans in words:
                        out = True
                        break
                    else:
                        out = False
                if out:
                    break

            if (ans in 'N') or (ans in 'n'):
                menu.run()
                return menu
            else:
                sys.exit(1)

    else:
        return menu


def menuSetup():
    mainMenu = menu.Menu("Main", 0)
    controlMenu = menu.SubMenu("Control", 1, mainMenu)
    monMenu = menu.SubMenu("Monitoring", 2, mainMenu)
    moduleMenu = menu.SubMenu("Module Status", 3, mainMenu)

    execOption1 = menu.ExecOption("set target value", 1, controlMenu, testfunction)
    autocontrol = menu.ToggleOption("control mode", 2, controlMenu, testfunction, 'Auto', 'Manual')

    return mainMenu


def testfunction():
    print("execute success")

#test
if __name__ == "__main__":
    #program = Popen(['lxterminal', '-e', 'python ./Foo.py'], stdout=PIPE)
    cmd_line()


'''
    1.control
        1) target value
        2) auto/manual
        3) 
    2.monitoring
        1) 
    3.peripheral status
        -> show category(actuator / sensor), i2c address
    4.
'''


