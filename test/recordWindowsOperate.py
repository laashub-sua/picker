# -*- coding:utf-8 -*-
from ctypes import wintypes, windll, Structure, c_int, c_uint, c_void_p, POINTER, cast, CFUNCTYPE

import win32api
import win32con
import win32gui
import win32process

# user32.dll,
SetWindowsHookEx = windll.user32.SetWindowsHookExA  # 将用户定义的钩子函数添加到钩子链中, 也就是我们的注册钩子函数
UnhookWindowsHookEx = windll.user32.UnhookWindowsHookEx  # 卸载钩子函数
CallNextHookEx = windll.user32.CallNextHookEx  # 在我们的钩子函数中必须调用, 这样才能让程序的传递消息
GetMessage = windll.user32.GetMessageA
GetModuleHandle = windll.kernel32.GetModuleHandleW
# 画笔
rectanglePen = win32gui.CreatePen(win32con.PS_SOLID, 3, win32api.RGB(255, 0, 0))

# 保存鼠标钩子函数句柄
mouse_hd = None


class POINT(Structure):
    _fields_ = [
        ('x', c_int),
        ('y', c_int)
    ]


class MSLLHOOKSTRUCT(Structure):
    _fields_ = [
        ('pt', POINT),
        ('hwnd', c_int),
        ('wHitTestCode', c_uint),
        ('dwExtraInfo', c_uint),
    ]


def wait_for_msg():
    msg = wintypes.MSG()
    GetMessage(msg, 0, 0, 0)


def mouse_pro(nCode, wParam, lParam):
    print('mouse_pro')
    """
    函数功能：鼠标钩子函数，当有鼠标事件，此函数被回调
    """
    if nCode == win32con.HC_ACTION:
        MSLLHOOKSTRUCT_p = POINTER(MSLLHOOKSTRUCT)
        param = cast(lParam, MSLLHOOKSTRUCT_p)
        # 鼠标左键点击
        if wParam == win32con.WM_LBUTTONDOWN:
            hForeWnd = win32gui.GetForegroundWindow()
            dwSelfThreadId = win32api.GetCurrentThreadId()
            print(dwSelfThreadId)
            dwForeThreadId = win32process.GetWindowThreadProcessId(hForeWnd)
            print(dwForeThreadId)
            win32process.AttachThreadInput(dwForeThreadId[1], dwSelfThreadId, True)
            hw = win32api.GetFocus()
            win32process.AttachThreadInput(dwForeThreadId[1], dwSelfThreadId, False)
            # hw = win32gui.WindowFromPoint(win32api.GetCursorPos())

            print("%s#######################%s" % (hw, mouse_hd))
            print(win32gui.GetClassName(hw))
            left, top, right, bottom = win32gui.GetWindowRect(hw)
            print(left, top, right, bottom)
            windowDc = win32gui.GetWindowDC(hw)
            if windowDc:
                prevPen = win32gui.SelectObject(windowDc, rectanglePen)
                prevBrush = win32gui.SelectObject(windowDc, win32gui.GetStockObject(win32con.HOLLOW_BRUSH))

                win32gui.Rectangle(windowDc, 0, 0, right - left, bottom - top)
                win32gui.SelectObject(windowDc, prevPen)
                win32gui.SelectObject(windowDc, prevBrush)
                win32gui.ReleaseDC(hw, windowDc)

            # hw = win32gui.WindowFromPoint((int(param.contents.pt.x),int(param.contents.pt.y)))
            # print("%s#######################%s" % (hw, mouse_hd))
            # print(win32gui.GetClassName(hw))
            # left, top, right, bottom = win32gui.GetWindowRect(hw)
            # print(left, top, right, bottom)
            # print("左键点击，坐标：x:%d,y:%d" % (param.contents.pt.x,param.contents.pt.y))
            # hwndChildList = get_child_windows(hw)
            # for hwndChild in hwndChildList:
            #     hw = hwndChild
            #     print("%s#######################%s" % (hw, mouse_hd))
            #     print(win32gui.GetClassName(hw))
            #     left, top, right, bottom = win32gui.GetWindowRect(hw)
            #     print(left, top, right, bottom)
            #     windowDc = win32gui.GetWindowDC(hw)
            #     if windowDc:
            #         prevPen = win32gui.SelectObject(windowDc, rectanglePen)
            #         prevBrush = win32gui.SelectObject(windowDc, win32gui.GetStockObject(win32con.HOLLOW_BRUSH))
            #
            #         win32gui.Rectangle(windowDc, 0, 0, right - left, bottom - top)
            #         win32gui.SelectObject(windowDc, prevPen)
            #         win32gui.SelectObject(windowDc, prevBrush)
            #         win32gui.ReleaseDC(hw, windowDc)

        # elif wParam == win32con.WM_LBUTTONUP:
        #     print("左键抬起，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
        # elif wParam == win32con.WM_MOUSEMOVE:
        #     hw = win32gui.WindowFromPoint(win32api.GetCursorPos())
        #     print("%s#######################%s" % (hw, mouse_hd))
        #     print(win32gui.GetClassName(hw))
        #     left, top, right, bottom = win32gui.GetWindowRect(hw)
        #     print(left, top, right, bottom)
        #     windowDc = win32gui.GetWindowDC(hw)
        #     if windowDc:
        #         prevPen = win32gui.SelectObject(windowDc, rectanglePen)
        #         prevBrush = win32gui.SelectObject(windowDc, win32gui.GetStockObject(win32con.HOLLOW_BRUSH))
        #
        #         win32gui.Rectangle(windowDc, 0, 0, right - left, bottom - top)
        #         win32gui.SelectObject(windowDc, prevPen)
        #         win32gui.SelectObject(windowDc, prevBrush)
        #         win32gui.ReleaseDC(hw, windowDc)
        #
        #     # hw = win32gui.WindowFromPoint((int(param.contents.pt.x),int(param.contents.pt.y)))
        #     # print("%s#######################%s" % (hw, mouse_hd))
        #     # print(win32gui.GetClassName(hw))
        #     # left, top, right, bottom = win32gui.GetWindowRect(hw)
        #     # print(left, top, right, bottom)
        #
        #     print("鼠标移动，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
        # elif wParam == win32con.WM_RBUTTONDOWN:
        #     print("右键点击，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
        # elif wParam == win32con.WM_RBUTTONUP:
        #     print("右键抬起，坐标：x:%d,y:%d" % (param.contents.pt.x, param.contents.pt.y))
    return CallNextHookEx(mouse_hd, nCode, wParam, lParam)


def get_child_windows(parent):
    '''
    获得parent的所有子窗口句柄
     返回子窗口句柄列表
     '''
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
    return hwndChildList


def start_mouse_hook():
    """
    函数功能：启动鼠标监听
    """
    print(c_void_p)
    HOOKPROTYPE = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    print(HOOKPROTYPE)
    pointer = HOOKPROTYPE(mouse_pro)
    global mouse_hd
    mouse_hd = SetWindowsHookEx(
        win32con.WH_MOUSE_LL,  # \钩子类型
        pointer,  # 回调函数地址
        GetModuleHandle(None),  # 实例句柄
        0  # 线程ID
    )



    wait_for_msg()


def stop_mouse_hook():
    """
    函数功能：停止鼠标监听
    """
    UnhookWindowsHookEx(mouse_hd)


if __name__ == '__main__':
    start_mouse_hook()
