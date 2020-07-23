import win32api
import win32con
import win32process
from win32gui import GetWindowRect, GetWindowText, EnumWindows, IsWindowVisible


def get_target_position_hwnd(target_mouse_position_x, target_mouse_position_y):
    data = []

    def callback(hwnd, param):
        (left, top, right, bottom) = GetWindowRect(hwnd)
        if target_mouse_position_x > right or target_mouse_position_x < left:
            return
        if target_mouse_position_y > bottom or target_mouse_position_y < top:
            return
        data.append(hwnd)

    EnumWindows(callback, None)
    for hwnd in data:
        window_text = GetWindowText(hwnd)
        if not window_text or window_text.strip() == '':
            continue
        if not IsWindowVisible(hwnd):
            continue
        return hwnd


def get_win_exe_path_and_title_by_hwnd(hwnd):
    title = GetWindowText(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    hndl = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, 0, pid)
    path = win32process.GetModuleFileNameEx(hndl, 0)
    return title, path


def do_derive(target_mouse_position_x, target_mouse_position_y):
    return get_win_exe_path_and_title_by_hwnd(
        get_target_position_hwnd(target_mouse_position_x, target_mouse_position_y))
