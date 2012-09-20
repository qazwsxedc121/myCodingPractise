'''
Created on 2012-5-20

@author: guoxc
'''
import Tkinter


def resize(ev=None):

    label.config(font='Helvetica -%d bold' % scale.get())


top=Tkinter.Tk()  

top.geometry('600x400')

label=Tkinter.Label(top,text='Hello world!',font='Helvetica -12 bold')

label.pack(fill=Tkinter.X,expand=1)


scale=Tkinter.Scale(top,from_=10,to=40,orient=Tkinter.HORIZONTAL,command=resize)

scale.set(12) 

scale.pack(fill=Tkinter.X,expand=1)

quit_button = Tkinter.Button(top,text='QUIT',command=top.quit,activeforeground='white',activebackground='red')

quit_button.pack()

Tkinter.mainloop()