import time
import curses

stdscr = curses.initscr()
begin_x = 20
begin_y = 7
height = 5
width = 40
win = curses.newwin(height, width, begin_y, begin_x)

time.sleep(10)