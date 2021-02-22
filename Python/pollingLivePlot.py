#   https://stackoverflow.com/questions/15736393/live-plot-in-python-gui

import tkinter as tk
import random

class ServoDrive(object):
    # simulate values
    def getVelocity(self): return random.randint(0, 50)
    def getTorque(self): return random.randint(50, 100)

class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.servo = ServoDrive()
        self.canvas = tk.Canvas(self, background="black", width=100, height=100)
        self.canvas.pack(side="top", fill="none", expand=False)

        # create lines for velocity and torque
        self.velocity_line = self.canvas.create_line(0, 0, 0, 0, fill="red")
        self.torque_line = self.canvas.create_line(0, 0, 0, 0, fill="blue")

        # start the update process
        self.update_plot()

    def update_plot(self):
        v = self.servo.getVelocity()
        t = self.servo.getTorque()
        self.add_point(self.velocity_line, v)
        self.add_point(self.torque_line, t)
        self.canvas.xview_moveto(1.0)
        self.after(100, self.update_plot)

    def add_point(self, line, y):
        coords = self.canvas.coords(line)
        x = coords[-2] + 1
        coords.append(x)
        coords.append(y)
        coords = coords[-200:] # keep # of points to a manageable size
        self.canvas.coords(line, *coords)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Welcome to LikeGeeks app")
    window.geometry('350x200')

    lbl1 = tk.Label(window, text="Hello")  # , font=("Arial Bold", 14))
    lbl1.pack(side="left")
    Example(window).pack(side="right", fill="both", expand=True)
    window.mainloop()