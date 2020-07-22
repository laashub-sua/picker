import threading

from pynput import keyboard
from pynput import mouse

"""
monitor the mouse: x, y
    paint the x, y, w, h box with red color
monitor the ctrl-keyboard
    generate the position index value
"""


def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))
    pass


def on_activate_h():
    print('on_activate_h')


def monitoring_mouse():
    with mouse.Listener(
            on_move=on_move) as listener:
        listener.join()
    mouse.Listener(
        on_move=on_move).start()


def monitoring_keyboard():
    with keyboard.GlobalHotKeys({'<ctrl>': on_activate_h}) as h:
        h.join()


threading.Thread(target=monitoring_mouse).start()
threading.Thread(target=monitoring_keyboard).start()

