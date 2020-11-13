import sys
import traceback
import os
import lcddriver
import keypaddriver


class Menu(object):
    def __init__(self, title, index):
        self.title = title
        self.menuIndex = index
        self.prevMenu = self
        self.subMenuObj = []
        self.display = lcddriver.lcd()
        self.button = keypaddriver.keypad()

    def run(self):
        self.menu_wrapper(self.lister)

    def istop(self):
        return self.title == self.prevMenu.title and self.menuIndex == self.prevMenu.menuIndex

    def lister(self):
        for i in range(self.subMenuObj.__len__()):
            print(self.subMenuObj[i].menuIndex, ' - ', self.subMenuObj[i].title, end='')
            if isinstance(self.subMenuObj[i], ToggleOption):
                print('  >>  Status / ', self.subMenuObj[i].getstatus())
            else:
                print('')

    def menu_wrapper(self, method, **kwargs):
        print('\n')
        for i in range(len(self.title) + 48):
            print("=", end='')
        print("\n", self.title)
        self.display.lcd_clear()
        self.display.lcd_long_write(self.display, self.title, 1)
        for i in range(len(self.title) + 48):
            print("=", end='')
        print("")

        method(**kwargs)

        for i in range(len(self.title) + 48):
            print("=", end='')
        print("\n0 - Back")
        for i in range(len(self.title) + 48):
            print("=", end='')


class SubMenu(Menu):
    def __init__(self, title, index, prevmenu, **kwargs):
        super().__init__(title, index)
        self.prevMenu = prevmenu
        prevmenu.subMenuObj.append(self)
        self.lister = kwargs.pop('lister')
        self.listkwargs = kwargs.pop('listkwargs')

    def lister(self, **kwargs):
        self.lister(**self.listkwargs)


# single executable option
class ExecOption(SubMenu):
    def __init__(self, title, index, prevmenu, **kwargs):
        super().__init__(title, index, prevmenu)
        self.function = kwargs.pop('function')
        self.funcargs = kwargs

    def opt_guide(self, str):
        # Explanation will go here
        print(str)

    def run(self):
        try:
            self.opt_guide('This is executable option for test')
            self.function(**self.funcargs)

        except:
            sys.stderr.write('executable option execution failed')


# queued executable option
class ExecOptionQ(ExecOption):
    def __init__(self, title, index, prevmenu, **kwargs):
        super().__init__(title, index, prevmenu, **kwargs)
        self.opq = kwargs.pop('opq')

    def run(self):
        try:
            print()
            self.opq.add(self.function, **self.funcargs)
            print(self.opq.queue.qsize())
        except:
            sys.stderr.write('executable option execution failed')


class ToggleOption(ExecOption):
    def __init__(self, title, index, prevmenu, **kwargs):
        super().__init__(title, index, prevmenu, **kwargs)
        self.toggleStatus = False
        self.function2 = kwargs.pop('function2')
        self.trueopt = kwargs.pop('trueopt', 'On')
        self.falseopt = kwargs.pop('falseopt', 'Off')

    def run(self):
        self.opt_guide('This is executable option for test')
        try:
            if self.toggleStatus is False:
                try:
                    print(self.function, self.funcargs)
                    self.function(**self.funcargs)
                    self.toggleStatus = not self.toggleStatus
                except:
                    print('run failure 1')
            else:
                try:
                    if self.function2 is not None:
                        print(self.function2, self.funcargs)
                        self.function2(**self.funcargs)
                        self.toggleStatus = not self.toggleStatus
                    else:
                        self.function(**self.funcargs)
                        self.toggleStatus = not self.toggleStatus
                except:
                    print('run failure 2')

        except:
            sys.stderr.write('executable option execution failed\n')

    def getstatus(self):
        if self.toggleStatus:
            return self.trueopt
        else:
            return self.falseopt
