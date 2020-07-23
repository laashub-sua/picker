import tkinter as tk

import win32gui
import win32print
from PIL import ImageGrab
from win32.lib import win32con
from win32api import GetSystemMetrics


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h


def get_screen_size():
    """获取缩放后的分辨率"""
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    return w, h


real_resolution = get_real_resolution()
screen_size = get_screen_size()

# Windows 设置的屏幕缩放率
# ImageGrab 的参数是基于显示分辨率的坐标，而 tkinter 获取到的是基于缩放后的分辨率的坐标
screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)


class Box:

    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

    def isNone(self):
        return self.start_x is None or self.end_x is None

    def setStart(self, x, y):
        self.start_x = x
        self.start_y = y

    def setEnd(self, x, y):
        self.end_x = x
        self.end_y = y

    def box(self):
        lt_x = min(self.start_x, self.end_x)
        lt_y = min(self.start_y, self.end_y)
        rb_x = max(self.start_x, self.end_x)
        rb_y = max(self.start_y, self.end_y)
        return lt_x, lt_y, rb_x, rb_y

    def center(self):
        center_x = (self.start_x + self.end_x) / 2
        center_y = (self.start_y + self.end_y) / 2
        return center_x, center_y


class SelectionArea:

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.area_box = Box()

    def empty(self):
        print('empty')
        return self.area_box.isNone()

    def setStartPoint(self, x, y):
        print('setStartPoint')
        self.canvas.delete('area', 'lt_txt', 'rb_txt')
        self.area_box.setStart(x, y)
        # 开始坐标文字
        self.canvas.create_text(
            x, y - 10, text=f'({x}, {y})', fill='red', tag='lt_txt')

    def updateEndPoint(self, x, y):
        print('updateEndPoint')
        self.area_box.setEnd(x, y)
        self.canvas.delete('area', 'rb_txt')
        box_area = self.area_box.box()
        # 选择区域
        self.canvas.create_rectangle(
            *box_area, fill='black', outline='red', width=2, tags="area")
        self.canvas.create_text(
            x, y + 10, text=f'({x}, {y})', fill='red', tag='rb_txt')


class ScreenShot():

    def __init__(self, scaling_factor=2):
        self.win = tk.Tk()
        # self.win.tk.call('tk', 'scaling', scaling_factor)
        self.width = self.win.winfo_screenwidth()
        self.height = self.win.winfo_screenheight()

        # 无边框，没有最小化最大化关闭这几个按钮，也无法拖动这个窗体，程序的窗体在Windows系统任务栏上也消失
        self.win.overrideredirect(True)
        self.win.attributes('-alpha', 0.1)

        self.is_selecting = False

        # 绑定按 Enter 确认, Esc 退出
        self.win.bind('<KeyPress-Escape>', self.exit)
        self.win.bind('<KeyPress-Return>', self.confirmScreenShot)
        self.win.bind('<Button-1>', self.selectStart)
        self.win.bind('<ButtonRelease-1>', self.selectDone)
        self.win.bind('<Motion>', self.changeSelectionArea)

        self.canvas = tk.Canvas(self.win, width=self.width,
                                height=self.height)
        self.canvas.pack()
        self.area = SelectionArea(self.canvas)

        # self.area.updateEndPoint(578.0, 239.0)


        self.win.mainloop()

    def exit(self, event):
        print('exit')
        self.win.destroy()

    def clear(self):
        print('clear')
        self.canvas.delete('area', 'lt_txt', 'rb_txt')
        self.win.attributes('-alpha', 0)

    def captureImage(self):
        print('captureImage')
        if self.area.empty():
            return None
        else:
            box_area = [x * screen_scale_rate for x in self.area.area_box.box()]
            self.clear()
            print(f'Grab: {box_area}')
            img = ImageGrab.grab(box_area)
            return img

    def confirmScreenShot(self, event):
        print('confirmScreenShot')
        img = self.captureImage()
        if img is not None:
            img.show()
        self.win.destroy()

    def selectStart(self, event):
        print('selectStart')
        self.is_selecting = True
        self.area.setStartPoint(event.x, event.y)
        # print('Select', event)

    def changeSelectionArea(self, event):
        print('changeSelectionArea')
        if self.is_selecting:
            self.area.updateEndPoint(event.x, event.y)
            # print(event)

    def selectDone(self, event):
        print('selectDone')
        # self.area.updateEndPoint(event.x, event.y)
        self.is_selecting = False


def main():
    ScreenShot()


if __name__ == '__main__':
    main()
