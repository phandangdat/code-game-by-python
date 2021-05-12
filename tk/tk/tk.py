#import tkinter as tk
from tkinter import *

#khởi tạo một cửa sổ
window = Tk()
#khai báo title cho cửa số
window.title("Cửa sổ game")
#lbl = Label(text="Xin chào người chơi")
#lbl.pack()
lbl = Label(window,text="Xin chào người chơi",font=("time new roman",20),fg="red")
lbl.grid(column=0,row=0)

etr = Entry(window,width=200)
etr.grid(column=1,row=2)

def xuly():
    print(etr.get())
def xoa():
    #print(type(etr.get()))
    for i in range(0,len(etr.get())):
        etr.delete(0)
btn = Button(window,text="Xuất",command=xuly,bg="orange",fg="red",font=(20))
btn.grid(column=1,row=0)
btn = Button(window,text="Reset",command=xoa,bg="orange",fg="red",font=(20))
btn.grid(column=2,row=0)
window.mainloop()
