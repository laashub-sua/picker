# try to get current windows
from win32gui import EnumWindows, GetWindowText, GetWindowRect


def get_window():
    data = []

    def callback(hwnd, param):
        (left, top, right, bottom) = GetWindowRect(hwnd)  # meanings that left-top point and right-bottom point
        size = (right - left) * (bottom - top)
        # if size <= 0:
        #     return
        # if left <= 0 and top <= 0 and right <= 0 and bottom <= 0:
        #     return
        window_text = GetWindowText(hwnd)
        # if not window_text or window_text.strip() == '':
        #     return

        # HDC = GetDC(hwnd)
        # DrawFocusRect(hDC, rc)
        # need get the window's z-index value for sort
        # print(window_text)
        # print(left, top, right, bottom)
        # print("-------------------------------------")
        data.append(hwnd)

    EnumWindows(callback, None)
    return data


window_list = get_window()
print(window_list)
if __name__ == '__main__':
    pass
