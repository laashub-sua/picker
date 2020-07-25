from pywinauto.application import Application

from component import derive_handle
from component import draw_rect


def tree_win(win):
    position_info = win.rectangle()  # L, T, R, B    # L52, T111, R1010, B151    # 相当于左上角和右下角两个点的坐标
    win_data = {}
    win_data['pos'] = (position_info.left, position_info.top, position_info.right, position_info.bottom)
    win_children = win.children()
    win_children_len = len(win_children)
    if win_children_len > 0:
        win_data['child'] = []
        for win_item in win_children:
            win_data['child'].append(tree_win(win_item))
    return win_data


def condition_win_panel_not_in_area(win_panel, target_mouse_position_x, target_mouse_position_y):
    position_info = win_panel.element_info.rectangle
    if target_mouse_position_x > position_info.right or target_mouse_position_x < position_info.left:
        return True
    if target_mouse_position_y > position_info.bottom or target_mouse_position_y < position_info.top:
        return True
    return False


# 当目标win由多层子win_panel组成时, 一直往下取; 取到最后, 留一个疑问是否有意义
# 当同一个点上多个win_panel时, 取z order值最大的一个win_panel
def get_handle_info(win_panel, target_mouse_position_x, target_mouse_position_y, win_position_level_arr):
    if condition_win_panel_not_in_area(win_panel, target_mouse_position_x, target_mouse_position_y):
        return
    # win_panel.print_control_identifiers()
    win_child_list = win_panel.children()
    if len(win_child_list) < 1:
        position_info = win_panel.element_info.rectangle
        draw_rect.do_draw(position_info.left, position_info.top, position_info.right - position_info.left,
                          position_info.bottom - position_info.top)
        for index in range(len(win_panel.criteria)):
            if index == 0:
                continue
            win_position_level_arr.append(win_panel.criteria[index])
        return
    for win_child in win_child_list:
        if condition_win_panel_not_in_area(win_child, target_mouse_position_x, target_mouse_position_y):
            continue
        automation_id = win_child.element_info.automation_id
        class_name = win_child.element_info.class_name
        rich_text = win_child.element_info.rich_text
        child_win_index = -1
        while True:
            child_win_index += 1
            try:
                win_panel_child = win_panel.child_window(title=rich_text, class_name=class_name, auto_id=automation_id,
                                                         found_index=child_win_index)
                if condition_win_panel_not_in_area(win_panel_child, target_mouse_position_x, target_mouse_position_y):
                    continue
                get_handle_info(win_panel_child, target_mouse_position_x, target_mouse_position_y,
                                win_position_level_arr)
            except Exception as e:
                break

        # try:
        #     win_panel_child.class_name()
        # except Exception as e:
        #     continue
        # break  # 暂略


def prepare_do_derive(execute_file_path, title, target_mouse_position_x, target_mouse_position_y):
    print('prepare_do_derive')
    app = Application().connect(path=execute_file_path)
    top_window = app.window(title=title)
    return top_window


top_window = None


def do_derive(target_mouse_position_x, target_mouse_position_y):
    path = r'C:\Program Files\FileZilla FTP Client\filezilla.exe'
    title = 'FileZilla'
    if not derive_handle.top_window:
        derive_handle.top_window = prepare_do_derive(path, title, target_mouse_position_x, target_mouse_position_y)
    win_position_level_arr = []
    try:
        get_handle_info(derive_handle.top_window, target_mouse_position_x, target_mouse_position_y,
                        win_position_level_arr)
        if len(win_position_level_arr) > 0:
            for item in win_position_level_arr:
                print(item)
                # print(item['class_name']+':'+item['title'])
    except Exception as e:
        print(e)
        pass
    print('----------------------')