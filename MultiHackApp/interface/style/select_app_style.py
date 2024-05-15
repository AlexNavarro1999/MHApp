from tkinter import colorchooser


def select_color():
    color = colorchooser.askcolor(title="Seleccionar color")
    if color[1]:
        return color[1]
