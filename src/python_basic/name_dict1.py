import Tkinter
import cPickle
import random

top = Tkinter.Tk()

word_dict = cPickle.load(file("../../data/SogouLabDicNew1.txt"))
str1 = Tkinter.StringVar()
label1 = Tkinter.Label(top, textvariable=str1)
label1.pack()
def callback():
    i = random.randrange(len(word_dict))
    while "N" not in word_dict[i][1]:
        i = random.randrange(len(word_dict))
    str1.set(word_dict[i][0])


button1 = Tkinter.Button(top, text="Run", command=callback)
button1.pack()
top.mainloop()