import sys
import os
from ModularHydroponics import menu


def cmd_line(menusetup):
    currentmenu = menusetup()
    currentmenu.run()
    while True:
        os.system('cls')
        cmd = input('\nSelect> ')
        try:
            currentmenu = handleoption(cmd, currentmenu)

        except KeyboardInterrupt:
            sys.exit(1)
            pass


def handleoption(cmd, men):
    if cmd.isdecimal() and int(cmd) > 0:
        try:
            if isinstance(men.subMenuObj[int(cmd)-1], menu.ExecOption) or isinstance(men.subMenuObj[int(cmd)-1], menu.ToggleOption):
                men.subMenuObj[int(cmd) - 1].run()
                men.run()
                return men
            else:
                men.subMenuObj[int(cmd) - 1].run()
                return men.subMenuObj[int(cmd) - 1]
        except:
            print('invalid submenu')
            return men

    elif cmd.isdecimal() and int(cmd) == 0:
        if not men.is_top():
            print('back to prevmenu')
            men.prevMenu.run()
            return men.prevMenu
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
                men.run()
                return men
            else:
                sys.exit(1)

    else:
        return men





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


