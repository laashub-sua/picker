import ctypes

import win32con


def get_window():
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


window_list = get_window()
print(window_list)
