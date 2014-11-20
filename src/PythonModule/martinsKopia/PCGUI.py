# PCGUI stub

#motor(L,R), arm(X,Y,Z,W,P,G), calibrate, status
#automotor(M), autoarm(M), start

from tkinter import *
from tkinter import ttk
#from pcModule import pcModule

#gloria=pcModule("localhost")
#gloria.updateSensors()
#gloria.start()

def main():
    
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
        #harcoded inputs are int, rest are py_var (StringVar)
        if isinstance(L, int) and isinstance(R, int):
            gloria.setMotorSpeed(L, R)
        else:
            gloria.setMotorSpeed(int(L.get()), int(R.get()))

    def write_arm(X,Y,Z,P,G):
        gloria.setArmPosition(int(X.get()), int(Y.get()), int(Z.get()), int(P.get()), int(W.get()), int(G.get()))

    def write_single(command):
        if command == "status":
            pass
            
    def write_auto(M):
        pass

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
        
    ttk.Label(mainframe, textvariable=motorL).grid(column=1, row=3)
    ttk.Button(mainframe, text="LMotor Val", command=motorL_get).grid(column=1, row=2)

    ttk.Label(mainframe, textvariable=motorR).grid(column=3, row=3)
    ttk.Button(mainframe, text="RMotor Val", command=motorR_get).grid(column=3, row=2)

    ttk.Button(mainframe, text="LR drive", command=lambda : write_motor(motorL, motorR)).grid(column=2, row=1)
    ttk.Button(mainframe, text="Spin left", command=lambda : write_motor(-50, 50)).grid(column=2, row=2)
    ttk.Button(mainframe, text="Spin right", command=lambda : write_motor(50, -50)).grid(column=2, row=3)
    ttk.Button(mainframe, text="Left turn", command=lambda : write_motor(50, 100)).grid(column=1, row=4)
    ttk.Button(mainframe, text="Right turn", command=lambda : write_motor(100, 50)).grid(column=3, row=4)

    #arm start
    X = StringVar() #any way to assign all these to StringVar at once... ?
    Y = StringVar()
    Z = StringVar()
    P = StringVar()
    Wr = StringVar()
    G = StringVar()

    X_entry = ttk.Entry(mainframe, width=7, textvariable=X)
    X_entry.grid(column=6, row=1, sticky=(W, E))
    ttk.Label(mainframe, text="X").grid(column=5, row=1, sticky=(W, E))
    Y_entry = ttk.Entry(mainframe, width=7, textvariable=Y)
    Y_entry.grid(column=6, row=2, sticky=(W, E))
    ttk.Label(mainframe, text="Y").grid(column=5, row=2, sticky=(W, E))
    Z_entry = ttk.Entry(mainframe, width=7, textvariable=Z)
    Z_entry.grid(column=6, row=3, sticky=(W, E))
    ttk.Label(mainframe, text="Z").grid(column=5, row=3, sticky=(W, E))
    P_entry = ttk.Entry(mainframe, width=7, textvariable=P)
    P_entry.grid(column=6, row=4, sticky=(W, E))
    ttk.Label(mainframe, text="P").grid(column=5, row=4, sticky=(W, E))
    W_entry = ttk.Entry(mainframe, width=7, textvariable=Wr)
    W_entry.grid(column=6, row=5, sticky=(W, E))
    ttk.Label(mainframe, text="W").grid(column=5, row=5, sticky=(W, E))
    G_entry = ttk.Entry(mainframe, width=7, textvariable=G)
    G_entry.grid(column=6, row=6, sticky=(W, E))
    ttk.Label(mainframe, text="G").grid(column=5, row=6, sticky=(W, E))

    ttk.Button(mainframe, text="Send to arm", command=lambda : write_arm(X, Y, Z, P, Wr, G)).grid(column=6, row=7)

    #status, calibrate

    #ttk.Button(mainframe, text="Status", command=lambda : write_single("status")).grid(column=  
    
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

main() #use only for local gui test
