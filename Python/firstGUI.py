#   Tutorial from https://likegeeks.com/python-gui-examples-tkinter-tutorial/
from tkinter import *
from tkinter.ttk import *

'''#    Test on Button State
buttonState = BooleanVar()
buttonState.set(False)
if buttonState:
    lbl2.configure("Button was clicked")
else:
    lbl2.configure("Click on Button")
buttonState.set(not buttonState)
'''

window = Tk()

window.title("Welcome to LikeGeeks app")
window.geometry('350x200')

'''#    Label, Button and Entry text
lbl1 = Label(window, text="Hello")#, font=("Arial Bold", 14))
lbl1.grid(column=0, row=0)
lbl2 = Label(window, text="Click on Button")
lbl2.grid(column=0, row=1)

txt = Entry(window, width=10, state='disabled')
txt.grid(column=1, row=0)
txt.focus()

def clicked():
    res = "Welcome to " + txt.get()
    lbl1.configure(text=res)

btn = Button(window, text="Click Me", command=clicked)#, bg="orange", fg="red")
btn.grid(column=2, row=0)
'''


'''#     Selection List
combo = Combobox(window)
combo['values'] = (1, 2, 3, 4, 5, "Text")
combo.current(1) #set the selected item
combo.grid(column=0, row=0)
#combo.get()
'''

'''#     Check Button
chk_state = BooleanVar()
chk_state.set(True) #set check state
chk = Checkbutton(window, text='Choose', var=chk_state)
chk.grid(column=0, row=0)
'''

'''#    Radio Button
selected = IntVar()

rad1 = Radiobutton(window, text='First', value=1, variable=selected)
rad2 = Radiobutton(window, text='Second', value=2, variable=selected)
rad3 = Radiobutton(window, text='Third', value=3, variable=selected)
rad1.grid(column=0, row=0)
rad2.grid(column=1, row=0)
rad3.grid(column=2, row=0)

def clicked():
   print(selected.get())
   
btn = Button(window, text="Click Me", command=clicked)
btn.grid(column=3, row=0)
'''

'''#    Scrolled Text
from tkinter import messagebox
txt = scrolledtext.ScrolledText(window, width=40, height=10)
txt.insert(INSERT, 'Your text goes here')
txt.grid(column=0, row=0)
'''

'''#   MessageBox
from tkinter import messagebox
def clicked():
    messagebox.showinfo('Message title', 'Message content')
    messagebox.showwarning('Message title', 'Message content')  # shows warning message
    messagebox.showerror('Message title', 'Message content')  # shows error message
    res = messagebox.askquestion('Message title', 'Message content')
    res = messagebox.askyesno('Message title', 'Message content')
    res = messagebox.askyesnocancel('Message title', 'Message content')
    res = messagebox.askokcancel('Message title', 'Message content')
    res = messagebox.askretrycancel('Message title', 'Message content')
btn = Button(window,text='Click here', command=clicked)
btn.grid(column=0, row=0)
'''

'''#   Spinbox
var = IntVar()
var.set(36)
spin1 = Spinbox(window, from_=0, to=100, width=5, textvariable=var)
spin2 = Spinbox(window, values=(3, 8, 11), width=5)
spin1.grid(column=0, row=0)
spin2.grid(column=1, row=0)
'''

'''#   Progressbar
from tkinter.ttk import Progressbar
from tkinter import ttk

style = ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background='black')

bar = Progressbar(window, length=200, style='black.Horizontal.TProgressbar')
bar['value'] = 70
bar.grid(column=0, row=0)
'''

'''#   filedialog
from tkinter import filedialog
from os import path

file = filedialog.askopenfilename(initialdir=path.dirname(__file__))
#dir = filedialog.askdirectory()
#file = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
'''

'''#Menu bar
from tkinter import Menu

menu = Menu(window)
new_item = Menu(menu, tearoff=0)
new_item.add_command(label='New') #, command=clicked)
new_item.add_separator()
new_item.add_command(label='Edit')
menu.add_cascade(label='File', menu=new_item)

window.config(menu=menu)
'''

'''#    Tab Control (Notebook widget)
from tkinter import ttk

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text='First')
tab_control.add(tab2, text='Second')

lbl1 = Label(tab1, text='label1')
lbl1.grid(column=0, row=0)
lbl2 = Label(tab2, text='label2')
lbl2.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')
'''

window.mainloop()

