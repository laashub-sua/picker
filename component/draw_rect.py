import queue
import threading
import tkinter as tk

import wx

from component import draw_rect

app = wx.App(False)
q = None


def prepare_refresh_screen():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-alpha', 0.01)
    root.state('zoomed')
    root.withdraw()
    draw_rect.q.put(root)
    root.mainloop()


def refresh_screen():
    root = draw_rect.q.get()
    draw_rect.q = queue.LifoQueue()
    root.state('zoomed')
    root.update()
    root.deiconify()
    root.withdraw()
    draw_rect.q.put(root)


draw_rect.q = queue.LifoQueue()
threading.Thread(target=prepare_refresh_screen).start()


def do_draw(x, y, width, height):
    dc = wx.ScreenDC()
    transparent_colour = wx.Colour(255, 255, 255, 0)

    red_colour = wx.Colour(255, 0, 0, 0)
    normal_pen = wx.Pen(red_colour, width=3)
    brush = wx.Brush(transparent_colour, style=wx.BRUSHSTYLE_TRANSPARENT)
    dc.SetBackgroundMode(wx.TRANSPARENT)

    refresh_screen()
    dc.DrawRectangleList([(x, y, width, height)], normal_pen, brush)
