import queue
import threading
import time
import tkinter as tk


def prepare_refresh_screen(q):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-alpha', 0.5)
    root.state('zoomed')
    root.withdraw()
    q.put(root)
    root.mainloop()


def refresh_screen(q):
    root = q.get()
    root.state('zoomed')
    root.update()
    root.deiconify()
    time.sleep(1)
    root.withdraw()
    q.put(root)


q = queue.Queue()
threading.Thread(target=prepare_refresh_screen, args=(q,)).start()

while True:
    time.sleep(1)
    print('while')
    refresh_screen(q)
