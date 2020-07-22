import os

from pywinauto.application import Application


def test_notepad():
    if os.path.exists('test.txt'):
        os.remove('test.txt')
    try:
        Application().start(r"C:\WINDOWS\system32\notepad.exe")  # 启动notepad
        app = Application().connect(path=r"C:\WINDOWS\system32\notepad.exe")  # 连接到notepad
        win_notepad = app[u"无标题 - 记事本"]
        win_notepad.print_control_identifiers()
        # # 点击帮助菜单
        # win_notepad.menu_select(u'帮助(H)->关于记事本(A)')
        # app[u'关于“记事本”'][u'确定'].click()
        # 输入值
        win_notepad.edit.type_keys(r'tristan 测试输入', with_spaces=True)

        win_notepad.close()
    except Exception as e:
        win_notepad.close()
        raise e


if __name__ == '__main__':
    test_notepad()
