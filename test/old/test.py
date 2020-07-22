import os

from pywinauto.application import Application


def test_notepad():
    if os.path.exists('test.txt'):
        os.remove('test.txt')

    # 打开一个记事本(如果已经打开，可以忽略)
    app = Application().start("notepad.exe")
    # 绑定进程,class_name和title是可选的，可以灵活使用，如果找到多个货没有找到该程序，程序会报错
    app = Application().connect(class_name="Notepad", title="无标题 - 记事本")

    # 得到可操作的窗口，可以传入标题，类名，或者将标题传入键值
    win = app.window(title="无标题 - 记事本")
    # 或者(通常使用此方法)
    win = app["无标题 - 记事本"]
    win.print_control_identifiers()


    # 可以使用Edit对可编辑区进行编辑
    win.Edit.type_keys('test.txt')
    win.menu_select("文件->保存")
    # 当弹出新的窗口时，窗口标题变化，因此需要重新确定可操作窗口
    win = app['另存为']
    win.Edit.type_keys('test.txt')
    # 窗口内含有的按钮等名称，同样可以作为键值传入，从而得到控件
    win['保存'].click()


if __name__ == '__main__':
    test_notepad()
