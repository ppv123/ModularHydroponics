import sys
import traceback
import LCD_driver
import time

import os


class Menu(object):
    def __init__(self, title, index):
        self.title = title
        self.menuIndex = index
        self.prevMenu = self
        self.subMenuObj = []  # 하위메뉴 목록 리스트들(딕셔너리 타입)
        self.display = LCD_driver.lcd()  # lcd 클래스의 인스턴스: display

    def lcd_write(self, display, text='', num_line=1, num_cols=15):
        if (len(text) > num_cols):
            display.lcd_display_string(text[:num_cols], num_line)
            for i in range(len(text) - num_cols + 1):
                text_to_print = text[i:i + num_cols]
                display.lcd_display_string(text_to_print, num_line)
                time.sleep(0.1)
            time.sleep(1)
        else:
            display.lcd_display_string(text, num_line)

    def run(self):
        self.menu_listing()

    def is_top(self):
        return self.title == self.prevMenu.title and self.menuIndex == self.prevMenu.menuIndex

    def menu_listing(self):  # 메뉴들을 화면에 표시
        print('\n')
        for i in range(len(self.title) + 48):
            print("=", end='')
        print("\n", self.title)
        self.display.lcd_clear()
        self.lcd_write(self.display, self.title, 1)
        for i in range(len(self.title) + 48):
            print("=", end='')
        print("")
        for i in range(self.subMenuObj.__len__()):
            print(self.subMenuObj[i].menuIndex, ' - ', self.subMenuObj[i].title, end='')
            self.lcd_write(self.display, 'go = ' + str(self.subMenuObj[i].menuIndex) + '-' + self.subMenuObj[i].title, 2)
            if isinstance(self.subMenuObj[i], ToggleOption):  # toggleoption 활성화
                print('  >>  Status / ', self.subMenuObj[i].getstatus())
            else:
                print('')
        # 아래는 '0 - Back' 출력
        for i in range(len(self.title) + 48):
            print("=", end='')
        print("\n0 - Back")
        self.lcd_write(self.display, 'go = 0-Back    ', 2)
        for i in range(len(self.title) + 48):
            print("=", end='')


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
            self.lcd_write(self.display, 'ExecOp', 2)

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
