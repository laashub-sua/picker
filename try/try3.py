import ctypes

import win32con
from win32gui import GetWindowRect, GetWindowText, EnumWindows, IsWindowVisible


def get_window():
    data = []

    def callback(hwnd, param):
        data.append(hwnd)

    EnumWindows(callback, None)
    return data


def get_ordered_window():
    '''Returns windows in z-order (top first)'''
    user32 = ctypes.windll.user32
    lst = []
    top = user32.GetTopWindow(None)
    if not top:
        return lst
    lst.append(top)
    while True:
        next = user32.GetWindow(lst[-1], win32con.GW_HWNDNEXT)
        if not next:
            break
        lst.append(next)
    return lst


target_value_x = 1258
target_value_y = 563


def get_target_position_window():
    data = []

    def callback(hwnd, param):
        (left, top, right, bottom) = GetWindowRect(hwnd)
        if target_value_x > right or target_value_x < left:
            return
        if target_value_y > bottom or target_value_y < top:
            return
        data.append(hwnd)

    EnumWindows(callback, None)
    target_hwnd = None
    for hwnd in data:
        window_text = GetWindowText(hwnd)
        if not window_text or window_text.strip() == '':
            continue
        if not IsWindowVisible(hwnd):
            continue
        target_hwnd = hwnd
        break
    window_text = GetWindowText(target_hwnd)
    print(window_text)

def try1():
    window_list = get_ordered_window()
    for hwnd in window_list:
        (left, top, right, bottom) = GetWindowRect(hwnd)
        if left <= 0 and top <= 0 and right <= 0 and bottom <= 0:
            continue
        window_text = GetWindowText(hwnd)
        if not window_text or window_text.strip() == '':
            continue
        if target_value_x > right or target_value_x < left:
            continue
        if target_value_y > bottom or target_value_y < top:
            continue
        if not IsWindowVisible(hwnd):
            continue
        print(window_text)
        print(left, top, right, bottom)
        print("-------------------------------------")


if __name__ == '__main__':
    # import time
    # time.sleep(3)
    # try1()
    get_target_position_window()
