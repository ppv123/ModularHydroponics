import sys
import os


class Menu(object):
    def __init__(self, title, index):
        # Ideally, self._options would be an empty dict for the base class.
        # This is just for the sake of example.
        self.title = title
        self.menuIndex = index
        self.prevMenu = self
        self.subMenuObj = []

    def run(self):
        self.menu_listing()

    def is_top(self):
        return self.title == self.prevMenu.title and self.menuIndex == self.prevMenu.menuIndex

    def menu_listing(self):
        print('\n')
        for i in range(len(self.title) + 48):
            print("=", end='')
        print("\n", self.title)
        for i in range(len(self.title) + 48):
            print("=", end='')
        print("")
        for i in range(self.subMenuObj.__len__()):
            print(self.subMenuObj[i].menuIndex, ' - ', self.subMenuObj[i].title, end='')
            if isinstance(self.subMenuObj[i], ToggleOption):
                print('  >>  Status / ', self.subMenuObj[i].getStatus())
            else:
                print('')

        for i in range(len(self.title)+48):
            print("=", end='')
        print("\n0 - Back")
        for i in range(len(self.title)+48):
            print("=", end='')


class SubMenu(Menu):
    def __init__(self, title, index, prevmenu):
        Menu.__init__(self, title, index)
        self.prevMenu = prevmenu
        prevmenu.subMenuObj.append(self)

#single executable option
class ExecOption(SubMenu):
    def __init__(self, title, index, prevmenu, function):
        SubMenu.__init__(self, title, index, prevmenu)
        self.function = function

    def opt_guide(self, *args):
        print('\nExplanation will go here')
        print(*args)

    def run(self, *args, **kwargs):
        try:
            self.opt_guide('This is executable option for test')
            self.function()
            #self.prevMenu.run()

        except:
            sys.stderr.write('executable option execution failed')

class ToggleOption(ExecOption):
    def __init__(self, title, index, prevmenu, function, *toggleopt):
        ExecOption.__init__(self, title, index, prevmenu, function)
        self.toggleStatus = False
        self.toggleOpt = []
        if toggleopt is not None:
            for opt in toggleopt:
                self.toggleOpt.append(opt)

    def run(self, *args, **kwargs):
        try:
            self.opt_guide('This is executable option for test')
            self.function()
            self.toggleStatus = not self.toggleStatus
            self.prevMenu.run()

        except:
            sys.stderr.write('executable option execution failed')

    def getStatus(self):
        if self.toggleOpt is not None:
            if self.toggleStatus:
                return self.toggleOpt[0]
            else:
                return self.toggleOpt[1]
        else:
            return self.toggleStatus