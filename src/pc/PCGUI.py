#!/usr/bin/python

#motor(L,R), arm(X,Y,Z,W,P,G), calibrate, status
#automotor(M), autoarm(M), start?

import sys
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from pcModule import pcModule

gloria=pcModule(str(sys.argv[1]))
#gloria=pcModule("192.168.99.1")
#gloria=pcModule("10.42.0.47")
gloria.updateSensors()
gloria.start()
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
            gloria.setMotorSpeed(-100, 100) #hard spin left
            motorL.set(-100)
            motorR.set(100)
            lastIssuedCommand.set("SpinLeft")
        elif button_pressed == 'e':
            gloria.setMotorSpeed(100, -100) #hard spin right
            motorL.set(100)
            motorR.set(-100)
            lastIssuedCommand.set("SpinRight")
        else:
            pass
        if button_pressed in ['w','s','r']:
            motorL.set(speed)
            motorR.set(speed)
        gloria.updateSensors()
        mainframe.focus_set()

    def write_arm(X,Y,Z,P,W,G):
        values = [e.get() for e in [X, Y, Z, P, W, G]]
        cocked = False

        for e in values:
            try:
                int(e)
            except ValueError:
                cocked = True

        if not cocked:
            gloria.setArmPosition(int(X.get()), int(Y.get()), int(Z.get()), int(P.get()), int(W.get()), int(G.get()))
            gloria.updateSensors()
            mainframe.focus_set()
        else:
            errorCodes.set("YOU COCKED UP MOTHERFUCKER! CYKA!")
        
    def write_single(command,arg):
        if command == "status":
            errorCodes.set(gloria.getErrorCodes())
            lineSensor.set(gloria.getLineSensor())
            leftDistance.set(gloria.getDistanceSensor()[0])
            rightDistance.set(gloria.getDistanceSensor()[1])
            calibration.set(gloria.getCalibration())
            armX.set(gloria.getArmPosition()[0])
            armY.set(gloria.getArmPosition()[1])
            armZ.set(gloria.getArmPosition()[2])
            armP.set(gloria.getArmPosition()[3])
            armW.set(gloria.getArmPosition()[4])
            armG.set(gloria.getArmPosition()[5])
            motorBool.set(gloria.getAutoMotor())
            armBool.set(gloria.getArmAuto())
            lastIssuedCommand.set("Got Status")
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
    ttk.Label(mainframe, text="Use W to accelerate").grid(column=4, row=1)
    ttk.Label(mainframe, text="Use S to slow down").grid(column=4, row=2)

    ttk.Button(mainframe, text="Debug test", command=lambda : write_motor(motorL, motorR)).grid(column=2, row=1)
    ttk.Button(mainframe, text="Hard left (Q)", command=lambda : write_motor(-50, 50)).grid(column=1, row=5)
    ttk.Button(mainframe, text="Hard right (E)", command=lambda : write_motor(50, -50)).grid(column=2, row=5)
    ttk.Button(mainframe, text="Spin left (A)", command=lambda : write_motor(50, 100)).grid(column=1, row=4)
    ttk.Button(mainframe, text="Spin right (D)", command=lambda : write_motor(100, 50)).grid(column=2, row=4)
    ttk.Button(mainframe, text="Stop (R)", command=lambda : write_motor(0, 0)).grid(column=3, row=4)

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

    
    
    #auto motor/arm
    ttk.Button(mainframe, text="AutoMotor", command=lambda : write_single("motor", True)).grid(column=1, row=6)
    ttk.Button(mainframe, text="ManMotor", command=lambda : write_single("motor", False)).grid(column=2, row=6)
    ttk.Button(mainframe, text="AutoArm", command=lambda : write_single("arm", True)).grid(column=1, row=7)
    ttk.Button(mainframe, text="ManArm", command=lambda : write_single("arm", False)).grid(column=2, row=7)
    ttk.Button(mainframe, text="GotPackage", command=lambda : write_single("hasPackage", True)).grid(column=3, row=7) #True is a bogus variable right now, but it allows support for True/False implementation if needed

    #status and calibrate
    ttk.Button(mainframe, text="Status", command=lambda : write_single("status",0)).grid(column=3, row=5)
    ttk.Button(mainframe, text="Calibrate", command=lambda : write_single("calibrate",0)).grid(column=3, row=6)

    errorCodes = StringVar()
    lineSensor = StringVar()
    lastIssuedCommand = StringVar()
    leftDistance = StringVar()
    rightDistance = StringVar()
    calibration = StringVar()
    armX = StringVar()
    armY = StringVar()
    armZ = StringVar()
    armP = StringVar()
    armW = StringVar()
    armG = StringVar()
    motorBool = StringVar()
    armBool = StringVar()
    
    ttk.Label(mainframe, text="errorCodes:").grid(column=1, row=8)
    ttk.Label(mainframe, textvariable=errorCodes).grid(column=2, row=8, columnspan=5)
    ttk.Label(mainframe, text="lineSensor:").grid(column=1, row=9)
    ttk.Label(mainframe, textvariable=lineSensor).grid(column=2, row=9, columnspan=5)
    #ttk.Label(mainframe, text="latest Command:").grid(column=3, row=9)
    #ttk.Label(mainframe, textvariable=lastIssuedCommand).grid(column=4, row=9)
    ttk.Label(mainframe, text="leftDistance:").grid(column=1, row=10)
    ttk.Label(mainframe, textvariable=leftDistance).grid(column=2, row=10)
    ttk.Label(mainframe, text="rightDistance:").grid(column=1, row=11)
    ttk.Label(mainframe, textvariable=rightDistance).grid(column=2, row=11)
    ttk.Label(mainframe, text="calibration:").grid(column=3, row=10)
    ttk.Label(mainframe, textvariable=calibration).grid(column=4, row=10)
    ttk.Label(mainframe, text="armX:").grid(column=1, row=12)
    ttk.Label(mainframe, textvariable=armX).grid(column=2, row=12)
    ttk.Label(mainframe, text="armY:").grid(column=3, row=12)
    ttk.Label(mainframe, textvariable=armY).grid(column=4, row=12)
    ttk.Label(mainframe, text="armZ:").grid(column=5, row=12)
    ttk.Label(mainframe, textvariable=armZ).grid(column=6, row=12)
    ttk.Label(mainframe, text="armP:").grid(column=1, row=13)
    ttk.Label(mainframe, textvariable=armP).grid(column=2, row=13)
    ttk.Label(mainframe, text="armW:").grid(column=3, row=13)
    ttk.Label(mainframe, textvariable=armW).grid(column=4, row=13)
    ttk.Label(mainframe, text="armG:").grid(column=5, row=13)
    ttk.Label(mainframe, textvariable=armG).grid(column=6, row=13)
    ttk.Label(mainframe, text="motorState:").grid(column=1, row=14)
    ttk.Label(mainframe, textvariable=motorBool).grid(column=2, row=14)
    ttk.Label(mainframe, text="armState:").grid(column=3, row=14)
    ttk.Label(mainframe, textvariable=armBool).grid(column=4, row=14)
    
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    #keybindings
    mainframe.focus_set()
    mainframe.bind("<Key>", keybind_motor)
    mainframe.pack()

    def update_status():
        write_single("status", 0)
        root.after(1000,update_status)
    root.after(1000,update_status)
    root.mainloop()

main() #use only for local gui test
