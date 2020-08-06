import win32api
import win32con
import win32process
from win32gui import GetWindowRect, GetWindowText, EnumWindows, IsWindowVisible

from . import derive_win_program


def get_target_position_hwnd(target_mouse_position_x, target_mouse_position_y):
    """
    get hwnd value what the target position's program
    :param target_mouse_position_x: target mouse position x
    :param target_mouse_position_y: target mouse position y
    :return:
    """
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
    """
    get window execute path value and title name by hwnd value in win32 api
    :param hwnd: hwnd value
    :return:
    """
    title = GetWindowText(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    hndl = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, 0, pid)
    path = win32process.GetModuleFileNameEx(hndl, 0)
    return title, path


last_target_mouse_position_x, last_target_mouse_position_y = None, None
last_path, last_title = None, None


def do_derive(target_mouse_position_x, target_mouse_position_y):
    """
    do derive
    :param target_mouse_position_x: target mouse position x
    :param target_mouse_position_y: target mouse position y
    :return:
    """
    if derive_win_program.last_target_mouse_position_x != target_mouse_position_x or derive_win_program.last_target_mouse_position_y != target_mouse_position_y:
        derive_win_program.last_title, derive_win_program.last_path = get_win_exe_path_and_title_by_hwnd(
            get_target_position_hwnd(target_mouse_position_x, target_mouse_position_y))
        print("derive_win_program: title: ", derive_win_program.last_title, 'path: ', derive_win_program.last_path)
    derive_win_program.last_target_mouse_position_x, derive_win_program.last_target_mouse_position_y = target_mouse_position_x, target_mouse_position_y
    return derive_win_program.last_title, derive_win_program.last_path
