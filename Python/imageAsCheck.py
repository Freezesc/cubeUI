import tkinter as tk
root = tk.Tk()

on_image = tk.PhotoImage(width=48, height=24)
off_image = tk.PhotoImage(width=48, height=24)
on_image.put(("green",), to=(0, 0, 23, 23))
off_image.put(("red",), to=(24, 0, 47, 23))

var1 = tk.IntVar(value=1)
var2 = tk.IntVar(value=0)
cb1 = tk.Checkbutton(root, image=off_image, selectimage=on_image, indicatoron=False,
                     onvalue=1, offvalue=0, variable=var1)
cb2 = tk.Checkbutton(root, image=off_image, selectimage=on_image, indicatoron=False,
                     onvalue=1, offvalue=0, variable=var2)

cb1.pack(padx=20, pady=10)
cb2.pack(padx=20, pady=10)

root.mainloop()