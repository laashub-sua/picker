from pywinauto.application import Application

"""
{'path': 'C:\\Program Files\\FileZilla FTP Client\\filezilla.exe', 'title': 'FileZilla'}
{'title': 'panel', 'class_name': 'wxWindowNR', 'auto_id': '', 'found_index': 2, 'top_level_only': False}
{'title': '快速连接(&Q)', 'class_name': 'Button', 'auto_id': '', 'found_index': 0, 'top_level_only': False}

"""
path = 'C:\\Program Files\\FileZilla FTP Client\\filezilla.exe'
title = 'FileZilla'
element_info_list = [
    {
        'title': 'panel',
        'class_name': 'wxWindowNR',
        'found_index': 2,
    }
    , {
        'title': '快速连接(&Q)',
        'class_name': 'Button',
        'found_index': 0,
    }
]


def test1():
    app = Application().connect(path=path)
    cur_level_window = app.window(title=title)
    for item in element_info_list:
        item_title = item['title']
        item_class_name = item['class_name']
        item_found_index = item['found_index']
        cur_level_window = cur_level_window.child_window(title=item_title, class_name=item_class_name,
                                                         found_index=item_found_index)
        cur_level_window.click()
        print(cur_level_window)


if __name__ == '__main__':
    test1()
