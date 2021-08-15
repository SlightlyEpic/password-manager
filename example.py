from tkinter import *
import tkinter.messagebox
from PIL import ImageTk,Image

#verify password
def verify(pwd,pin):
	if True:
		wind()
	else:
		tkinter.messagebox.showinfo('Wrong Password','Wrong credentials. Please try again.')



#main window
def wind():
	# log.destroy()
	win=Tk()
	win.geometry('800x600')
	win.resizeable(0,0)
	win.title('Password Manager')
	Label(win,text='main').pack()
	win.mainloop()



#login page
def login():
	log=Tk()
	log.geometry('360x90')
	log.title('Login')
	log.resizable(0,0)

	lpwd = Label(log, text='Password :',font=('TkTextFont',10),padx=5,pady=5)
	lpin = Label(log, text='PIN :',font=('TkTextFont',10),padx=5,pady=5)
	epwd = Entry(log,show='\u2022',width=40)
	epin = Entry(log,show='\u2022',width=40)
	bt = Button(log, text='OK',font=('TkTextFont',10), fg='blue',width=5,command=lambda:verify(epwd.get(),epin.get()))
	lpwd.grid(row=1,column=1)
	lpin.grid(row=2,column=1)
	epwd.grid(row=1,column=2)
	epin.grid(row=2,column=2)
	bt.grid(row=3,column=2)


	log.mainloop()