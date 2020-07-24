import queue
import threading
import tkinter as tk

import wx

app = wx.App(False)


def prepare_refresh_screen(q):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-alpha', 0.01)
    root.state('zoomed')
    root.withdraw()
    q.put(root)
    root.mainloop()


def refresh_screen(q):
    root = q.get()
    root.state('zoomed')
    root.update()
    root.deiconify()
    root.withdraw()
    q.put(root)


q = queue.Queue()
threading.Thread(target=prepare_refresh_screen, args=(q,)).start()


def draw_rect(x, y, width, height):
    dc = wx.ScreenDC()
    transparent_colour = wx.Colour(255, 255, 255, 0)

    red_colour = wx.Colour(255, 0, 0, 0)
    normal_pen = wx.Pen(red_colour, width=3)
    brush = wx.Brush(transparent_colour, style=wx.BRUSHSTYLE_TRANSPARENT)
    dc.SetBackgroundMode(wx.TRANSPARENT)

    refresh_screen(q)
    dc.DrawRectangleList([(x, y, width, height)], normal_pen, brush)


"""
    # while True:
    #     dc.DrawRectangleList([(x, y, width, height)], normal_pen, brush)
    #     time.sleep(0.5)
"""
"""
    transparent_pen = wx.Pen(transparent_colour, width=3, style=wx.PENSTYLE_TRANSPARENT)
    is_not_first_draw = False
    while True:
        if is_not_first_draw:
            dc.DrawRectangleList([(x, y, width, height)], transparent_pen, brush)
            pass
        is_not_first_draw = True
        item = 0
        x, y, width, height = x + item, y + item, width + item, height + item
        dc.DrawRectangleList([(x, y, width, height)], normal_pen, brush)
        time.sleep(0.5)
"""

"""
    transparent_pen = wx.Pen(transparent_colour, width=3, style=wx.PENSTYLE_TRANSPARENT)
    is_not_first_draw = False
    # for item in range(100):
    #     if is_not_first_draw:
    #         dc.DrawRectangleList([(last_x, last_y, last_width, last_height)], transparent_pen, brush)
    #         pass
    #     is_not_first_draw = True
    #     last_x, last_y, last_width, last_height = x + item, y + item, width + item, height + item
    #     dc.DrawRectangleList([(last_x, last_y, last_width, last_height)], normal_pen, brush)
    #     time.sleep(0.5)
"""
# draw_rect(60, 60, 120, 120)
