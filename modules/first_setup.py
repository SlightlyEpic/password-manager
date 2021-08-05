from tkinter import *
import manager as mg
from PIL import ImageTk,Image


man=mg.Manager()
#first time window

f=Tk()
f.geometry('360x90')
f.title('First time setup')
f.resizable(0,0)

lpwd = Label(f, text='Set Password :',font=('TkTextFont',10),padx=5,pady=5)
lpin = Label(f, text='Set PIN :',font=('TkTextFont',10),padx=5,pady=5)
epwd = Entry(f,width=40)
epin = Entry(f,width=40)
bt = Button(f, text='OK',font=('TkTextFont',10), fg='blue',width=5,command=lambda:man.genKey(epwd.get(),epin.get()))
lpwd.grid(row=1,column=1)
lpin.grid(row=2,column=1)
epwd.grid(row=1,column=2)
epin.grid(row=2,column=2)
bt.grid(row=3,column=2)


f.mainloop()