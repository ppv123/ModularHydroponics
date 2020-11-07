import sys
import traceback

import os


class Menu(object):
    def __init__(self, title, index):
        self.title = title
        self.menuIndex = index
        self.prevMenu = self
        self.subMenuObj = []    #하위메뉴 목록 리스트들(딕셔너리 타입)
        #self.disp1602mode = False

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
            if isinstance(self.subMenuObj[i], ToggleOption):    #toggleoption 활성화
                print('  >>  Status / ', self.subMenuObj[i].getstatus())
            else:
                print('')
        #아래는 '0 - Back' 출력
        for i in range(len(self.title) + 48):
            print("=", end='')
        print("\n0 - Back")
        for i in range(len(self.title) + 48):
            print("=", end='')


'''
    def menu_1902(self):
        if self.disp1602mode in True:
            #두줄씩 표시
            #표시 못하고 넘어가는 내용은 임시저장
            #키보드조작(다음으로 넘어갈때) 나머지 메뉴 표시
'''
class SubMenu(Menu):
    def __init__(self, title, index, prevmenu):
        super().__init__(title, index)
        self.prevMenu = prevmenu
        prevmenu.subMenuObj.append(self)


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
