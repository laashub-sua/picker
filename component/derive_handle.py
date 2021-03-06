from pywinauto.application import Application

from component import derive_handle
from component import derive_win_program
from component import draw_rect

"""
derive handle
"""


def tree_win(win):
    """
    get the window children tree
    :param win: win object
    :return:
    """
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
    """
    condition window panel is in target area
    :param win_panel: window children panel object
    :param target_mouse_position_x: the target mouse position  x
    :param target_mouse_position_y: the target mouse position y
    :return:
    """
    position_info = win_panel.element_info.rectangle
    if target_mouse_position_x > position_info.right or target_mouse_position_x < position_info.left:
        return True
    if target_mouse_position_y > position_info.bottom or target_mouse_position_y < position_info.top:
        return True
    return False


# 当目标win由多层子win_panel组成时, 一直往下取; 取到最后, 留一个疑问是否有意义
# 当同一个点上多个win_panel时, 取z order值最大的一个win_panel
def get_handle_info(win_panel, target_mouse_position_x, target_mouse_position_y, win_position_level_arr):
    """
    get handle info
    :param win_panel: window panel object
    :param target_mouse_position_x: target mouse position x
    :param target_mouse_position_y: target mouse position y
    :param win_position_level_arr:  the array for window position
    :return:
    """
    if condition_win_panel_not_in_area(win_panel, target_mouse_position_x, target_mouse_position_y):
        return
    # win_panel.print_control_identifiers()
    win_child_list = win_panel.children()
    if len(win_child_list) < 1:
        position_info = win_panel.element_info.rectangle
        draw_rect.do_draw(position_info.left, position_info.top, position_info.right - position_info.left,
                          position_info.bottom - position_info.top)
        if len(win_panel.criteria) < 1:
            return
        win_position_level_arr.clear()
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
                break
            except Exception as e:
                break
        break


def prepare_do_derive(execute_file_path, title):
    """
    prepare for do derive
    :param execute_file_path: execute file path for program
    :param title: the title of window
    :return:
    """
    app = Application().connect(path=execute_file_path)
    top_window = app.window(title=title)
    return top_window


top_window = None

last_title, last_path = None, None


def do_derive(target_mouse_position_x, target_mouse_position_y):
    """
    do derive
    :param target_mouse_position_x:  target mouse position x
    :param target_mouse_position_y:  target mouse position y
    :return:
    """
    title, path = derive_win_program.get_win_exe_path_and_title_by_hwnd(
        derive_win_program.get_target_position_hwnd(target_mouse_position_x, target_mouse_position_y))
    if derive_handle.last_title != title or derive_handle.last_path != path:
        derive_handle.top_window = prepare_do_derive(path, title)
    derive_handle.last_title, derive_handle.last_path = title, path
    win_position_level_arr = []
    try:
        get_handle_info(derive_handle.top_window, target_mouse_position_x, target_mouse_position_y,
                        win_position_level_arr)
        if len(win_position_level_arr) < 1:
            return
        print('拾取控件成功')
        print({'path': path, 'title': title})
        for item in win_position_level_arr:
            print(item)

    except Exception as e:
        print(e)
        pass
    print('----------------------')
