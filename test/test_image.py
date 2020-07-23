left, top, right, bottom = 166, 56, 303, 84
import tkinter as tk
from turtle import RawTurtle, TurtleScreen, ScrolledCanvas

root = tk.Tk()
# width, height = root.winfo_screenwidth(), root.winfo_screenheight()
width, height = right - left, bottom - top
root.overrideredirect(True)
root.attributes('-alpha', 0.1)

# We're not scrolling but ScrolledCanvas has useful features
canvas = ScrolledCanvas(root)
canvas.pack(fill=tk.BOTH, expand=tk.YES)

screen = TurtleScreen(canvas)
# root.state('zoomed')
# window_width, window_height = screen.window_width(), screen.window_height()
# if window_width / width < window_height / height:
#     height = window_height / (window_width / width)
# else:
#     width = window_width / (window_height / height)
# screen.setworldcoordinates(-width / 2, -height / 2, width / 2 - 1, height / 2 - 1)

turtle = RawTurtle(screen)
turtle.color('red', 'red')
turtle.speed('fastest')
turtle.pensize(4)


# left, top, right, bottom = 100, 100, 900, 900

def draw_rect(left, top, right, bottom):
    turtle.penup()
    turtle.goto(left, top)  # left, top
    turtle.pendown()
    turtle.goto(right, top)
    turtle.goto(right, bottom)
    turtle.goto(left, bottom)
    turtle.goto(left, top)
    turtle.penup()


draw_rect(left, top, right, bottom)

screen.mainloop()
