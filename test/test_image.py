left, top, right, bottom = 166, 56, 303, 84
import tkinter as tk
from turtle import RawTurtle, TurtleScreen, ScrolledCanvas

root = tk.Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(True)
root.attributes('-alpha', 0.08)

canvas = ScrolledCanvas(root)
canvas.pack(fill=tk.BOTH, expand=tk.YES)

screen = TurtleScreen(canvas)
root.state('zoomed')

turtle = RawTurtle(screen)
turtle.color('red', 'red')
turtle.speed('fastest')
turtle.pensize(4)


# left, top, right, bottom = 100, 100, 900, 900

# def draw_rect(left, top, right, bottom):
#     turtle.penup()
#     turtle.goto(left, top)  # left, top
#     turtle.pendown()
#     turtle.goto(right, top)
#     turtle.goto(right, bottom)
#     turtle.goto(left, bottom)
#     turtle.goto(left, top)
#     turtle.penup()
#
#
# draw_rect(left, top, right, bottom)

# screen.mainloop()
