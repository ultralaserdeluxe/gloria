# PCGUI stub

#motor(L,R), arm(X,Y,Z,P,G), calibrate, status
#automotor(M), autoarm(M), start

from tkinter import *
from tkinter import ttk

def maintest():
    root = Tk()
    root.title("Gloria GUI command panel")
    scale = ttk.Scale(root, from_=0, to=100)
    scale.pack()
    root.mainloop()
    
#maintest()

def main():

##    file = open("command.txt", "w")
##    file.write(message)
##    file.close()
    def scale_get():
        try:
            number_entry = int(scale_entry.get())
            number.set(number_entry)
        except ValueError:
            pass
        
    root = Tk()
    root.title("Gloria GUI command centre")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    number = StringVar()

    scale_entry = ttk.Scale(mainframe, from_=0, to=100)
    scale_entry.grid(column=1, row=1, sticky=(W, E))
    scale_entry.pack()
        
    ttk.Label(mainframe, textvariable=number).grid(column=1, row=3, sticky=(W, E))
    ttk.Button(mainframe, text="Get Number", command=scale_get).grid(column=1, row=2, sticky=(W))
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

main() #use only for local gui test
