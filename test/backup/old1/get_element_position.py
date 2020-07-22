import json
import logging
import time

from pywinauto.application import Application

logging.basicConfig(level='INFO')
str_file_path = r"C:\Program Files\FileZilla FTP Client\filezilla.exe"


def tree_win(win):
    # L, T, R, B
    # L52, T111, R1010, B151
    # 相当于左上角和右下角两个点的坐标
    position_info = win.rectangle()
    win_data = {
        "position_info": position_info,
        "win_children": []
    }
    win_children = win.children()
    win_children_len = len(win_children)
    if win_children_len > 0:
        for win_item in win_children:
            win_data["win_children"].append(tree_win(win_item))
    return win_data


def test(win_filezilla):
    win_panel = win_filezilla.child_window(title=u"panel", auto_id="-31808", control_type="Pane")
    win_data = tree_win(win_panel)
    print(json.dumps(win_data, sort_keys=True, indent=4, separators=(',', ':')))
    win_panel.print_control_identifiers()


if __name__ == '__main__':
    execute_file_path = str_file_path
    Application().start(execute_file_path)
    app = Application(backend='uia').connect(path=execute_file_path)
    win_filezilla = app.window(title=u'FileZilla')
    try:
        test(win_filezilla)
        time.sleep(100)
        win_filezilla.close()
    except Exception as e:
        win_filezilla.close()
        raise e
