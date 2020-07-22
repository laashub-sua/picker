from pywinauto.application import Application


def test():
    execute_file_path = r"C:\Program Files\FileZilla FTP Client\filezilla.exe"
    Application().start(execute_file_path)
    app = Application(backend='uia').connect(path=execute_file_path)
    win_fz = app.window(title=u'FileZilla')
    win_fz.print_control_identifiers(depth=2)
    win_fz.wait('visible')

    # win_check_update = app['检查更新']
    # win_check_update.print_control_identifiers(depth=1)
    # # title="Contains:", auto_id="13087", control_type="UIA_ButtonControlTypeId"
    # # win_close = win_fz.window(title='关闭(C)', control_type="UIA_ButtonControlTypeId", auto_id='5101')
    # # if win_close:
    # #     win_close.close()
    #
    # win_check_update.window(title='关闭(C)', control_type="UIA_ButtonControlTypeId", auto_id='5101')
    # # win_host.type_keys(u'192.168.71.52')


if __name__ == '__main__':
    test()
