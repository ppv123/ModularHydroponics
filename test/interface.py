import sys
import os
import menu
import time
import lcddriver
import keypaddriver

display = lcddriver.lcd()
button = keypaddriver.keypad()


def cmd_line(menusetup, **kwargs):
    global instN
    currentmenu = menusetup(**kwargs)
    currentmenu.run()
    i = 0
    while True:
        # os.system('cls')
        #cmd = input('\nSelect> ')
        while len(currentmenu.subMenuObj)+1 > i:
            if len(currentmenu.subMenuObj)+1 == i:
                i = 0
                continue

            if i == 0:
                display.lcd_long_write(display, '0-Back', 2)

            if i != 0:
                display.lcd_long_write(display, '>' + str(currentmenu.title[i-1].menuIndex) + '-' + currentmenu.subMenuObj[i-1].title, 2)
            putB = button.key_input()
            if putB:
                i += 1
            elif not putB:
                cmd = str(i)
                i = 0
                break


        try:
            currentmenu = handleoption(cmd, currentmenu)

        except KeyboardInterrupt:
            sys.exit(1)
            pass


def handleoption(cmd, men):
    if cmd.isdecimal() and int(cmd) > 0:  # 'cmd' 가 정수이고, 1이상인가
        try:
            if isinstance(men.subMenuObj[int(cmd) - 1], menu.ExecOption or menu.ToggleOption):
                men.subMenuObj[int(cmd) - 1].run()
                men.run()
                return men
            elif isinstance(men, menu.ExecOptionList):
                stat = men.funcdic[int(cmd) - 1][0](men.funcdic[int(cmd) - 1][2])
                if stat is not None:
                    men.togglestat[int(cmd) - 1] = stat
            else:
                men.subMenuObj[int(cmd) - 1].run()
                return men.subMenuObj[int(cmd) - 1]
        except:
            print('invalid submenu')
            return men

    elif cmd.isdecimal() and int(cmd) == 0:  # 'cmd' 가 정수이고, 0인가
        if not men.is_top():
            print('back to prevmenu')
            men.prevMenu.run()
            return men.prevMenu
        else:  # men.is_top == True
            while True:
                # ans = input('Quit program? Y/N>> ')
                display.lcd_clear()
                display.lcd_write(display, 'Quit program? Y/N>> ', 1)
                putB = button.key_input()
                if putB == 0:
                    display.lcd_long_write(display, 'system off', 2)
                    time.sleep(1)
                    display.lcd_clear()
                    ans = 'y'
                elif putB != 0:
                    display.lcd_long_write(display, 'go to menu', 2)
                    time.sleep(1)
                    ans = 'n'

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
