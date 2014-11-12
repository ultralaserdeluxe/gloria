# PCGUI stub

#motor(L,R), arm(X,Y,Z,P,G), calibrate, status
#automotor(M), autoarm(M), start

from tkinter import *
from tkinter import ttk

def main():

##    file = open("command.txt", "w")
##    file.write(message)
##    file.close()
    
    def motorL_get():
        try:
            number_entry = int(motorL_entry.get())
            motorL.set(number_entry)
        except ValueError:
            pass

    def motorR_get():
        try:
            number_entry = int(motorR_entry.get())
            motorR.set(number_entry)
        except ValueError:
            pass
        
    def write_motor(L,R):
        file = open("command.txt", "w")
        file.write("motor=" + L.get() + ',' + R.get())
        file.close()

    def write_arm(X,Y,Z,P,G):
        file = open("command.txt", "w")
        file.write("arm=" + X.get() + ',' + Y.get() + ',' + Z.get() + ',' + P.get() + ',' + G.get())
        file.close()

    #mainframe start        
    root = Tk()
    root.title("Gloria GUI command centre")

    motorL = StringVar()
    motorR = StringVar()

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    #motor start

    motorL_entry = ttk.Scale(mainframe, from_=-100, to=100)
    motorL_entry.grid(column=1, row=1, sticky=(W, E))
    motorL_entry.pack()

    motorR_entry = ttk.Scale(mainframe, from_=-100, to=100)
    motorR_entry.grid(column=3, row=1, sticky=(W, E))
    motorR_entry.pack()
        
    ttk.Label(mainframe, textvariable=motorL).grid(column=1, row=3, sticky=(W, E))
    ttk.Button(mainframe, text="LMotor Val", command=motorL_get).grid(column=1, row=2, sticky=(W))

    ttk.Label(mainframe, textvariable=motorR).grid(column=3, row=3, sticky=(W, E))
    ttk.Button(mainframe, text="RMotor Val", command=motorR_get).grid(column=3, row=2, sticky=(W))

    ttk.Button(mainframe, text="LR drive", command=lambda : write_motor(motorL, motorR)).grid(column=2, row=1)

    #arm start
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

main() #use only for local gui test
