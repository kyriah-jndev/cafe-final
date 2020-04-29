from tkinter import *

root = Tk()
frame = Frame(root)
frame.place(x = 0, y = 0)
y = 0
x = 0
for ran in range(30):
    for run in range(30):
        bottomframe = Label(root, text ="O")
        bottomframe.place(x = x, y = y)
        y += 15
    x += 15


root.geometry("1920x1080")
root.mainloop()
