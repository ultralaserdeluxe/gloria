# PCGUI stub

#motor(L,R), arm(X,Y,Z,W,P,G), calibrate, status
#automotor(M), autoarm(M), start?

from tkinter import *
from tkinter import ttk
from pcModule import pcModule

gloria=pcModule("localhost")
gloria.updateSensors()
gloria.start()

def main():
    
    def motorL_get():
        try:
            temp = int(motorL_entry.get())
            motorL.set(temp)
        except ValueError:
            pass

    def motorR_get():
        try:
            temp = int(motorR_entry.get())
            motorR.set(temp)
        except ValueError:
            pass
        
    def write_motor(L,R):
        #harcoded inputs are int, rest are py_var (StringVar)
        if isinstance(L, int) and isinstance(R, int):
            gloria.setMotorSpeed(L, R)
        else:
            gloria.setMotorSpeed(int(L.get()), int(R.get()))
        gloria.updateSensors()

    def write_arm(X,Y,Z,P,W,G):
        #gloria.setArmPosition(100, 100, 100, 100, 100, 100)
        gloria.setArmPosition(int(X.get()), int(Y.get()), int(Z.get()), int(P.get()), int(W.get()), int(G.get()))
        gloria.updateSensors()
        
    def write_single(command,arg):
        if command == "status":
            print("error codes:")
            print(gloria.getErrorCodes())
            print("linesensor:")
            print(gloria.getLineSensor())
            print("left distance")
            print(gloria.getDistanceSensor()[0])
            print("right distance")
            print(gloria.getDistanceSensor()[1])
            print("armposition X:")
            print(gloria.getArmPosition()[0])
            print("armposition Y:")
            print(gloria.getArmPosition()[1])
            print("armposition Z:")
            print(gloria.getArmPosition()[2])
            print("armposition Pitch:")
            print(gloria.getArmPosition()[3])
            print("armposition wrist:")
            print(gloria.getArmPosition()[4])
            print("armposition grip:")
            print(gloria.getArmPosition()[5])
            print("latest calibration was done:")
            print(gloria.getCalibration())
            print("motors in auto mode:")
            print(gloria.getAutoMotor())
            print("arm in auto mode: ")
            print(gloria.getArmAuto())
        elif command == "calibrate":
            gloria.calibrate()
            #reply needed? check designspec
        elif command == "motor":
            if arg:
                gloria.setAutoMotor(True)
            else:
                gloria.setAutoMotor(False)
        elif command == "arm":
            if arg:
                gloria.setAutoArm(True)
            else:
                gloria.setAutoArm(False)
        gloria.updateSensors()
                
    #mainframe
    root = Tk()
    root.title("Gloria GUI command centre")

    motorL = StringVar()
    motorR = StringVar()

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    #motor
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
    ttk.Button(mainframe, text="Stop", command=lambda : write_motor(0, 0)).grid(column=2, row=4)

    #arm
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
    errorCodes = StringVar()
    lineSensor = StringVar()
    leftDistance = StringVar()
    rightDistance = StringVar()
    armX = StringVar()
    armY = StringVar()
    armZ = StringVar()
    armP = StringVar()
    armW = StringVar()
    armG = StringVar()
    calibration = StringVar()
    motorBool = StringVar()
    armBool = StringVar()

    ttk.Button(mainframe, text="Status", command=lambda : write_single("status",0)).grid(column=1, row=5)
    ttk.Button(mainframe, text="Calibrate", command=lambda : write_single("calibrate",0)).grid(column=2, row=5)

    #auto motor/arm
    ttk.Button(mainframe, text="AutoMotor", command=lambda : write_single("motor", True)).grid(column=1, row=6)
    ttk.Button(mainframe, text="ManMotor", command=lambda : write_single("motor", False)).grid(column=2, row=6)
    ttk.Button(mainframe, text="AutoArm", command=lambda : write_single("arm", True)).grid(column=1, row=7)
    ttk.Button(mainframe, text="ManArm", command=lambda : write_single("arm", False)).grid(column=2, row=7)
    
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

main() #use only for local gui test