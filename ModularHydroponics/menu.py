import sys
import traceback
import os


class Menu(object):
    def __init__(self, title, index):
        self.title = title
        self.menuIndex = index
        self.prevMenu = self
        self.subMenuObj = []

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
        for i in range(len(self.title) + 48):
            print("=", end='')
        print("")

        method(**kwargs)

        for i in range(len(self.title)+48):
            print("=", end='')
        print("\n0 - Back")
        for i in range(len(self.title)+48):
            print("=", end='')


class SubMenu(Menu):
    def __init__(self, title, index, prevmenu, **kwargs):
        super().__init__(title, index)
        self.prevMenu = prevmenu
        prevmenu.subMenuObj.append(self)



#single executable option
class ExecOption(SubMenu):
    def __init__(self, title, index, prevmenu, **kwargs):
        super().__init__(title, index, prevmenu)
        self.function = kwargs.pop('function', None)
        self.funcargs = kwargs

    def opt_guide(self):
        guide = self.funcargs.pop('optguide', None)
        if guide:
            print(guide)

    def run(self):
        try:
            if self.function:
                self.function(**self.funcargs)

        except:
            sys.stderr.write('executable option execution failed')

class ExecOptionList(ExecOption):
    def __init__(self, title, index, prevmenu, **kwargs):
        super().__init__(title, index, prevmenu, **kwargs)
        self.funcdic = kwargs.pop('funcdic', None)      #{0: (func0, name, kwargs0), 1: (func1, name, kwargs1), ...}
        self.trueopt = kwargs.pop('trueopt', 'On')
        self.falseopt = kwargs.pop('falseopt', 'Off')
        self.togglestat = list(None for i in range(len(self.funcdic)))

    def lister(self):
        if self.function:
            self.function(**self.funcargs)
        if self.funcdic:
            for index in range(len(self.funcdic)):
                print(index, '-', self.funcdic[index][1], ' ', self.funcdic[index][0].__name__, end='')
                if self.togglestat[index] is not None:
                    if self.togglestat[index]:
                        stat = self.trueopt
                    else:
                        stat = self.falseopt
                    print('>>', stat)
                else:
                    print('')

    def run(self):
        self.menu_wrapper(self.lister)


class ToggleOption(ExecOption):
    def __init__(self, title, index, prevmenu, **kwargs):
        super().__init__(title, index, prevmenu, **kwargs)
        self.toggleStatus = False
        self.function2 = kwargs.pop('function2')
        self.trueopt = kwargs.pop('trueopt', 'On')
        self.falseopt = kwargs.pop('falseopt', 'Off')
        self.funcargs = kwargs

    def run(self):
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


