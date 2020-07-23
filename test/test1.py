from component import derive_handle
from component import derive_win_program


def test_derive_win_program():
    title, path = derive_win_program.do_derive(551, 423)
    print(title, path)


def test_derive_handle():
    path = r'C:\Program Files\FileZilla FTP Client\filezilla.exe'
    title = 'FileZilla'
    target_mouse_position_x = 551
    target_mouse_position_y = 423
    derive_handle.do_derive(path, title, target_mouse_position_x, target_mouse_position_y)

def test_monitor_operation():
    pass
if __name__ == '__main__':
    # test_derive_win_program()
    # test_derive_handle()
    test_monitor_operation()
    pass
