import queue
import threading

from pynput import keyboard
from pynput import mouse

from component import derive_handle
from component import monitor_operation

trigger_event_thread = None
q = None


def trigger_event():
    while True:
        x, y = monitor_operation.q.get()
        monitor_operation.q = queue.LifoQueue()
        try:
            derive_handle.do_derive(x, y)
        except Exception as e:
            print(e)


def on_move(x, y):
    if not monitor_operation.trigger_event_thread:
        monitor_operation.q = queue.LifoQueue()
        monitor_operation.trigger_event_thread = threading.Thread(target=trigger_event)
        monitor_operation.trigger_event_thread.start()
    monitor_operation.q.put((x, y), block=True)


def on_activate_h():
    # print('on_activate_h')
    pass


def monitoring_mouse():
    with mouse.Listener(
            on_move=on_move) as listener:
        listener.join()
    mouse.Listener(
        on_move=on_move).start()


def monitoring_keyboard():
    with keyboard.GlobalHotKeys({'<ctrl>': on_activate_h}) as h:
        h.join()


def do_monitoring():
    threading.Thread(target=monitoring_mouse).start()
    threading.Thread(target=monitoring_keyboard).start()
