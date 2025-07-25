from tkinter import *
root=Tk()
root.geometry("444x333")
root.title("Yash Ka GUI")
title_label= Label(text="Yash Raut is one of the finest man on this planet earth " ,
                   bg ="red", fg="white" , padx=113,
                   pady=123 ,font=("comicsansms", 19, "bold")
                   , borderwidth=3, relief=SUNKEN)
title_label.pack(side=TOP, anchor="ne", fill=X)
#pack options
#anchor=north east=ne
#side=top,bottom,left,right(CAPITAL ME)(sab pack ke andar likhana
#padega.anchor ke saath use karna padega side.
#fill=X,Y


root.mainloop()
