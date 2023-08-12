from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename , askopenfilename
import subprocess
import os

file_path = ""

def set_file_path(path):

    global file_path
    file_path = path

def open_file():

    global code

    path = askopenfilename(filetypes = [('Squig scripts','*.sg')])
    with open(path) as script:
        program = script.read()
        code.delete('1.0',END)
        code.insert('1.0',program)
        set_file_path(path)

def save_file():

    if file_path == "":
        path = asksaveasfilename(filetypes = [('Squig scripts', '*.sg')])
    else:
        path = file_path

    with open(path , 'w') as script:
        code_script = code.get('1.0',END)
        script.write(code_script)
        set_file_path(path)

def run_file():

    if file_path == "":
        messagebox.showerror("Squig script", "Save")
        return
    

root = Tk()

root.title("SQUIG Shell")
root.geometry("1600x720")

root.configure(bg="#323846")

code = Text(root)
code.place(x = 100  , y = 0 , width = 2000 , height = 1200)

output  = Text(root , fg = "black")
output.place( x = 1250 , y = 0 , width = 2000 , height = 1200)

Button(root,text="Open",bd=0,command=open_file).place(x=30 , y = 260)
Button(root,text="Save" , bd=0,command=save_file).place(x=30 , y=145)
Button(root,text="Run",bd=0,command=run_file).place(x=30 , y = 30)

root.mainloop()

