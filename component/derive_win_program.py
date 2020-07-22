import win32api
import win32con
import win32process
from win32gui import GetWindowRect, GetWindowText, EnumWindows, IsWindowVisible


def get_target_position_hwnd(target_value_x, target_value_y):
    data = []

    def callback(hwnd, param):
        (left, top, right, bottom) = GetWindowRect(hwnd)
        if target_value_x > right or target_value_x < left:
            return
        if target_value_y > bottom or target_value_y < top:
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
