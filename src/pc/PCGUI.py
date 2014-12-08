#!/usr/bin/python

#motor(L,R), arm(X,Y,Z,W,P,G), calibrate, status
#automotor(M), autoarm(M), start?

import sys
from tkinter import *
from tkinter import ttk
from pcModule import pcModule

#gloria=pcModule(str(sys.argv[1]))
#gloria=pcModule("192.168.99.1")
#gloria=pcModule("10.42.0.47")
#gloria.updateSensors()
#gloria.start()
speed = 0

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
        #primarily a debugger now, not used for keybinds
        #harcoded inputs are int, rest are py_var (StringVar)
        if isinstance(L, int) and isinstance(R, int):
            Ltemp = L
            Rtemp = R
            L = StringVar()
            R = StringVar()
            L.set(Ltemp)
            R.set(Rtemp)
        else:
            #could probably be written better but it works
            Ltemp = int(motorL_entry.get())
            L.set(Ltemp)
            Rtemp = int(motorR_entry.get())
            R.set(Rtemp)
        gloria.setMotorSpeed(int(L.get()), int(R.get()))
        if Ltemp == Rtemp:
            if Ltemp == 0:
                lastIssuedCommand.set("Stopped")
            else:
                lastIssuedCommand.set("MovingStraight")
        elif Ltemp < Rtemp:
            lastIssuedCommand.set("TurningLeft")
        elif Ltemp > Rtemp:
            lastIssuedCommand.set("TurningRight")
        else:
            pass
        gloria.updateSensors()
        mainframe.focus_set()

    def keybind_motor(event=None):
        global speed
        #if time permits implement a dictionary instead
        button_pressed = event.char
        if button_pressed == 'w' and speed < 100:
            speed += 10
            gloria.setMotorSpeed(speed, speed) #faster
            lastIssuedCommand.set("IncrSpeed")
        elif button_pressed == 'a':
            if lastIssuedCommand.get() == "TurnLeft":
                gloria.setMotorSpeed(speed, speed) #stop turning
                motorL.set(speed)
                motorR.set(speed)
                lastIssuedCommand.set("StopTurn")
            else:
                gloria.setMotorSpeed(-speed, speed) #left turn
                motorL.set(-speed)
                motorR.set(speed)
                lastIssuedCommand.set("TurnLeft")
        elif button_pressed == 'd':
            if lastIssuedCommand.get() == "TurnRight":
                gloria.setMotorSpeed(speed, speed) #stop turning
                motorL.set(speed)
                motorR.set(speed)
                lastIssuedCommand.set("StopTurn")
            else:
                gloria.setMotorSpeed(speed, -speed) #right turn
                motorL.set(speed)
                motorR.set(-speed)
                lastIssuedCommand.set("TurnRight")
        elif button_pressed == 's' and speed > -100:
            speed -= 10
            gloria.setMotorSpeed(speed, speed) #slower
            lastIssuedCommand.set("DecrSpeed")
        elif button_pressed == 'r':
            gloria.setMotorSpeed(0, 0) #stop
            speed = 0
            lastIssuedCommand.set("Stopped")
        elif button_pressed == 'q':
            gloria.setMotorSpeed(-100, 100) #could also be -speed, speed
            #Might be nice for the motor, however it would require us to move
            #before we can spin. A separate function could be implemented for this.
            motorL.set(-50)
            motorR.set(50)
            lastIssuedCommand.set("SpinLeft")
        elif button_pressed == 'e':
            gloria.setMotorSpeed(100, -100) #same as above
            motorL.set(50)
            motorR.set(-50)
            lastIssuedCommand.set("SpinRight")
        else:
            pass
        if button_pressed in ['w','s','r']:
            motorL.set(speed)
            motorR.set(speed)
        gloria.updateSensors()
        mainframe.focus_set()

    def write_arm(X,Y,Z,P,W,G):
        gloria.setArmPosition(int(X.get()), int(Y.get()), int(Z.get()), int(P.get()), int(W.get()), int(G.get()))
        gloria.updateSensors()
        mainframe.focus_set()
        
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
            lastIssuedCommand.set("Calibrating")
            #reply needed? check designspec
        elif command == "motor":
            if arg:
                gloria.setAutoMotor(True)
                lastIssuedCommand.set("Motor Auto")
            else:
                gloria.setAutoMotor(False)
                lastIssuedCommand.set("Motor Manual")
        elif command == "arm":
            if arg:
                gloria.setAutoArm(True)
                lastIssuedCommand.set("Arm Auto")
            else:
                gloria.setAutoArm(False)
                lastIssuedCommand.set("Arm Manual")
        elif command == "hasPackage":
            gloria.setPackageTrue()
            lastIssuedCommand.set("Got Package")
        gloria.updateSensors()
        mainframe.focus_set()
                
    #mainframe
    root = Tk()
    root.title("Gloria GUI command centre")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    #motor
    motorL = StringVar()
    motorR = StringVar()
    
    motorL_entry = ttk.Scale(mainframe, from_=-100, to=100)
    motorL_entry.grid(column=1, row=1)

    motorR_entry = ttk.Scale(mainframe, from_=-100, to=100)
    motorR_entry.grid(column=3, row=1)
    
    ttk.Label(mainframe, textvariable=motorL).grid(column=1, row=3)
    ttk.Button(mainframe, text="LMotor Val", command=motorL_get).grid(column=1, row=2)

    ttk.Label(mainframe, textvariable=motorR).grid(column=3, row=3)
    ttk.Button(mainframe, text="RMotor Val", command=motorR_get).grid(column=3, row=2)

    ttk.Button(mainframe, text="LR drive", command=lambda : write_motor(motorL, motorR)).grid(column=2, row=1)
    ttk.Button(mainframe, text="Spin left (Q)", command=lambda : write_motor(-50, 50)).grid(column=2, row=2)
    ttk.Button(mainframe, text="Spin right (E)", command=lambda : write_motor(50, -50)).grid(column=2, row=3)
    ttk.Button(mainframe, text="Left turn (A)", command=lambda : write_motor(50, 100)).grid(column=1, row=4)
    ttk.Button(mainframe, text="Right turn (D)", command=lambda : write_motor(100, 50)).grid(column=3, row=4)
    ttk.Button(mainframe, text="Stop (R)", command=lambda : write_motor(0, 0)).grid(column=2, row=4)

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

    #status, calibrate, necessity depends on how we want to read status
    lastIssuedCommand = StringVar()
##    errorCodes = StringVar()
##    lineSensor = StringVar()
##    leftDistance = StringVar()
##    rightDistance = StringVar()
##    armX = StringVar()
##    armY = StringVar()
##    armZ = StringVar()
##    armP = StringVar()
##    armW = StringVar()
##    armG = StringVar()
##    calibration = StringVar()
##    motorBool = StringVar()
##    armBool = StringVar()

    ttk.Button(mainframe, text="Status", command=lambda : write_single("status",0)).grid(column=1, row=5)
    ttk.Button(mainframe, text="Calibrate", command=lambda : write_single("calibrate",0)).grid(column=2, row=5)
    ttk.Label(mainframe, textvariable=lastIssuedCommand).grid(column=3, row=5)
    
    #auto motor/arm
    ttk.Button(mainframe, text="AutoMotor", command=lambda : write_single("motor", True)).grid(column=1, row=6)
    ttk.Button(mainframe, text="ManMotor", command=lambda : write_single("motor", False)).grid(column=2, row=6)
    ttk.Button(mainframe, text="AutoArm", command=lambda : write_single("arm", True)).grid(column=1, row=7)
    ttk.Button(mainframe, text="ManArm", command=lambda : write_single("arm", False)).grid(column=2, row=7)
    ttk.Button(mainframe, text="GotPackage", command=lambda : write_single("hasPackage", True)).grid(column=3, row=7)
    
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    #keybindings
    mainframe.focus_set()
    mainframe.bind("<Key>", keybind_motor)
    mainframe.pack()

    root.mainloop()

main() #use only for local gui test
