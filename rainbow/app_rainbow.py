from tkinter import *

colors_cods = ['#ff0000', '#ff7d00', '#ffff00', '#00ff00', '#007dff', '#0000ff', '#7d00ff']
colors_name = ['red', 'orange', 'yellow', 'green', 'lightblue', 'blue', 'purple']


def paint_color(color, color_cod) -> None:
    label.config(text=color, fg=color)
    entry.config(color_code_text.set(color_cod), bg=color_cod)


root = Tk()
label = Label(text='Color name')
label.pack()

color_code_text = StringVar()
entry = Entry(textvariable=color_code_text)
entry.pack()

for i, color in enumerate(colors_cods):
    Button(bg=color, text=i + 1, command=lambda cod=color, name=colors_name[i]: paint_color(cod, name)).pack(fill=X)
root.mainloop()
