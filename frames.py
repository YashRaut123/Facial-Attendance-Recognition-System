from tkinter import *
root=Tk()
root.geometry("888x125")
fl = Frame(root, bg="grey", borderwidth=6, relief=SUNKEN)
fl.pack(side=LEFT, fill="y")
f2=Frame(root,bg="grey", borderwidth=8, relief=SUNKEN)
f2.pack(side=TOP, fill= "x")
lb= Label(fl, text="Yash is Great. \nNow we are creating a tkinter Project",bg="yellow"
          , borderwidth=6)
lb.pack(pady=142)
l2=Label(f2, text="Welcome to sublime text",
         borderwidth=8)
l2.pack()


root.mainloop()