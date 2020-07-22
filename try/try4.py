from component import derive_win_program

if __name__ == '__main__':
    # target_hwnd = get_target_position_hwnd(1258, 563)
    title, path = derive_win_program.get_win_exe_path_and_title_by_hwnd(
        derive_win_program.get_target_position_hwnd(551, 423))
    print(title, path)
