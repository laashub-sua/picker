import logging
import time

from pywinauto.application import Application

logging.basicConfig(level='INFO')
str_file_path = r"C:\Program Files\FileZilla FTP Client\filezilla.exe"
test_data = {
    "host": u"192.168.121.138",
    "username": u"root",
    "password": u"tsl0615",
    "port": u"22",
}
"""
在使用inspect.exe时:
Name            -> title
AutomationId    -> auto_id
ClassName       -> control_type

从顶层窗口开始往下层找, 使用child_window
"""


def test(win_filezilla):
    win_panel = win_filezilla.child_window(title=u"panel", auto_id="-31808", control_type="Pane")
    win_panel.print_control_identifiers(depth=2)
    win_panel.child_window(title=u"主机(H):", auto_id="-31805", control_type="Edit").type_keys(
        test_data['host'], with_spaces=True)  # 主机
    win_panel.child_window(title="用户名(U):", auto_id="-31803", control_type="Edit").type_keys(
        test_data['username'], with_spaces=True)  # 用户名
    win_panel.child_window(title="密码(W):", auto_id="-31801", control_type="Edit").type_keys(
        test_data['password'], with_spaces=True)  # 密码
    win_panel.child_window(title="端口(P):", auto_id="-31799", control_type="Edit").type_keys(
        test_data['port'], with_spaces=True)  # 端口
    win_panel.child_window(title="快速连接(Q)", auto_id="-31929", control_type="Button").click()  # 快速连接


if __name__ == '__main__':
    execute_file_path = str_file_path
    Application().start(execute_file_path)
    app = Application(backend='uia').connect(path=execute_file_path)
    win_filezilla = app.window(title=u'FileZilla')
    try:
        test(win_filezilla)
        time.sleep(10)
        win_filezilla.close()
    except Exception as e:
        win_filezilla.close()
        raise e
