import Tkinter as tk
import time
import socket  
import pcModule
import os
import math
import numpy as np
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pygame
class Joystick():
    def __init__(self,toControl=""):
        pygame.init()
        self.__init=False
        if toControl=="motor":
            name="Madcatz"
        if toControl=="arm":
            name="Saitek"
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joy=pygame.joystick.Joystick(i)
            joy.init()
            temp=joy.get_name()
            if name in temp:
                self.joystick=joy
                self.__init=True
                
    def get_init(self):
        return self.__init
    def x_axis(self):
        pygame.event.pump()
        return self.joystick.get_axis(0)
    def y_axis(self):
        pygame.event.pump()
        return self.joystick.get_axis(1)
    def axis2(self):
        pygame.event.pump()
        return self.joystick.get_axis(2)
    def axis3(self):
        pygame.event.pump()
        return self.joystick.get_axis(3)
    def axis4(self):
        pygame.event.pump()
        return self.joystick.get_axis(4)
    def get_button_0(self):
        pygame.event.pump()
        return self.joystick.get_button(0)
    def get_button_1(self):
        pygame.event.pump()
        return self.joystick.get_button(1)
    def get_button_2(self):
        pygame.event.pump()
        return self.joystick.get_button(2)
    def get_button_3(self):
        pygame.event.pump()
        return self.joystick.get_button(3)
    def get_button_4(self):
        pygame.event.pump()
        return self.joystick.get_button(4)
    def get_button_5(self):
        pygame.event.pump()
        return self.joystick.get_button(5)
    def get_button_6(self):
        pygame.event.pump()
        return self.joystick.get_button(6)
    def get_hat(self):
        pygame.event.pump()
        return self.joystick.get_hat(0)
    
class Gui():     
    def __init__(self):
        self.setup()
        
    def setup(self):
        #everything regarding gloria
        self.__ip_adress=""
        self.__gloria=None
        self.__motorJoy=None
        self.__armJoy=None
        #setup the root windows
        self.__root=tk.Tk()
        self.__root.resizable(True, True)
        self.__screenWidth=int(self.__root.winfo_screenwidth()*0.6)
        self.__screenHeight=int(self.__root.winfo_screenheight()*0.6)
        self.__root.minsize(self.__screenWidth,self.__screenHeight)
        self.__root.grid()
        self.__root.title("Glorious as FUCK")
        self.__root.config(bg='white')
        self.__root.update()
        self.__window_width=self.__root.winfo_width()
        self.__window_height=self.__root.winfo_height()
        self.__buttonsToEnable=[]
        self.__screenSaver=True
        self.__oldRegulatorErrors=[0.0 for e in range(100)]
        self.__oldRegulatorTime=[float(e) for e in range(100)]
        self.__oldRegulatorCounter=0
        #linesensors bars frame
        self.__linesensorFrame=tk.Frame(self.__root,bg="white",width=self.__window_width,height=self.__window_height/6)
        self.__linesensorFrame.grid(row = 0, column = 0,columnspan=5)
        #to be able to resize
        self.__root.rowconfigure(0,weight=1)
        self.__root.rowconfigure(1,weight=1)
        self.__root.rowconfigure(2,weight=1)
        self.__root.rowconfigure(3,weight=1)
        self.__root.rowconfigure(4,weight=1)
        self.__root.rowconfigure(5,weight=1)
        self.__root.rowconfigure(6,weight=1)
        self.__root.columnconfigure(0,weight=1)
        self.__root.columnconfigure(1,weight=1)
        self.__root.columnconfigure(2,weight=1)
        self.__root.columnconfigure(3,weight=1)
        self.__root.columnconfigure(4,weight=1)
        
        #linesensor bars
        self.__linesensorCanvas=tk.Canvas(self.__linesensorFrame,width=self.__window_width,height=self.__window_height/6)
        self.__linesensorCanvas.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        self.__bars={}
        self.__bar0=self.__linesensorCanvas.create_rectangle(int(self.__window_width*(1.0/18.0+0.0*(1.0/12.0))),int(self.__window_height/6),int(self.__window_width*(1.0/12.0+0.0*(1.0/12.0))),int(self.__window_height/6)-10,fill="black")
        self.__bars[0]=self.__bar0
        self.__bar1=self.__linesensorCanvas.create_rectangle(int(self.__window_width*(1.0/18.0+1.0*(1.0/12.0))),int(self.__window_height/6),int(self.__window_width*(1.0/12.0+1.0*(1.0/12.0))),int(self.__window_height/6)-20,fill="black")
        self.__bars[1]=self.__bar1
        self.__bar2=self.__linesensorCanvas.create_rectangle(int(self.__window_width*(1.0/18.0+2.0*(1.0/12.0))),int(self.__window_height/6),int(self.__window_width*(1.0/12.0+2.0*(1.0/12.0))),int(self.__window_height/6)-30,fill="black")
        self.__bars[2]=self.__bar2
        self.__bar3=self.__linesensorCanvas.create_rectangle(int(self.__window_width*(1.0/18.0+3.0*(1.0/12.0))),int(self.__window_height/6),int(self.__window_width*(1.0/12.0+3.0*(1.0/12.0))),int(self.__window_height/6)-40,fill="black")
        self.__bars[3]=self.__bar3
        self.__bar4=self.__linesensorCanvas.create_rectangle(int(self.__window_width*(1.0/18.0+4.0*(1.0/12.0))),int(self.__window_height/6),int(self.__window_width*(1.0/12.0+4.0*(1.0/12.0))),int(self.__window_height/6)-50,fill="black")
        self.__bars[4]=self.__bar4
        self.__bar5=self.__linesensorCanvas.create_rectangle(int(self.__window_width*(1.0/18.0+5.0*(1.0/12.0))),int(self.__window_height/6),int(self.__window_width*(1.0/12.0+5.0*(1.0/12.0))),int(self.__window_height/6)-60,fill="black")
        self.__bars[5]=self.__bar5
        self.__bar6=self.__linesensorCanvas.create_rectangle(int(self.__window_width*(1.0/18.0+6.0*(1.0/12.0))),int(self.__window_height/6),int(self.__window_width*(1.0/12.0+6.0*(1.0/12.0))),int(self.__window_height/6)-50,fill="black")
        self.__bars[6]=self.__bar6
        self.__bar7=self.__linesensorCanvas.create_rectangle(int(self.__window_width*(1.0/18.0+7.0*(1.0/12.0))),int(self.__window_height/6),int(self.__window_width*(1.0/12.0+7.0*(1.0/12.0))),int(self.__window_height/6)-40,fill="black")
        self.__bars[7]=self.__bar7
        self.__bar8=self.__linesensorCanvas.create_rectangle(int(self.__window_width*(1.0/18.0+8.0*(1.0/12.0))),int(self.__window_height/6),int(self.__window_width*(1.0/12.0+8.0*(1.0/12.0))),int(self.__window_height/6)-30,fill="black")
        self.__bars[8]=self.__bar8
        self.__bar9=self.__linesensorCanvas.create_rectangle(int(self.__window_width*(1.0/18.0+9.0*(1.0/12.0))),int(self.__window_height/6),int(self.__window_width*(1.0/12.0+9.0*(1.0/12.0))),int(self.__window_height/6)-20,fill="black")
        self.__bars[9]=self.__bar9
        self.__bar10=self.__linesensorCanvas.create_rectangle(int(self.__window_width*(1.0/18.0+10.0*(1.0/12.0))),int(self.__window_height/6),int(self.__window_width*(1.0/12.0+10.0*(1.0/12.0))),int(self.__window_height/6)-10,fill="black")
        self.__bars[10]=self.__bar10
        #connect frame
        self.__connectFrame=tk.Frame(self.__root,bg="white",width=self.__window_width/4,height=self.__window_height*2/6)
        self.__connectFrame.grid(row = 2, column = 0)
        self.__ip_entry = tk.Entry(self.__connectFrame)
        self.__ip_entry.place(relx=0.50,rely=0.30,anchor=tk.CENTER)
        self.__ip_entry.delete(0, tk.END)
        self.openConfigFile()
        self.__ip_entry.insert(0, self.__ip_adress)
        self.__connect_button=tk.Button(self.__connectFrame, text="connect", width=15, command=self.connectFunction)
        self.__connect_button.place(relx=0.50,rely=0.50,anchor=tk.CENTER)

        
        self.__connectArmJoystickButton=tk.Button(self.__connectFrame, text="connect arm joystick", width=15, command=self.connectArmJoystick)
        self.__connectArmJoystickButton.place(relx=0.50,rely=0.70,anchor=tk.CENTER)
        
        self.__connectMotorJoystickButton=tk.Button(self.__connectFrame, text="connect motor joystick", width=15, command=self.connectMotorJoystick)
        self.__connectMotorJoystickButton.place(relx=0.50,rely=0.90,anchor=tk.CENTER)
        
        self.__middleSeparator0=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__middleSeparator0.grid(row = 3, column = 0,sticky=tk.E+tk.W)
        
        self.__middleSeparator1=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__middleSeparator1.grid(row = 3, column = 1,sticky=tk.E+tk.W)
        
        self.__middleSeparator2=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__middleSeparator2.grid(row = 3, column = 2,sticky=tk.E+tk.W)
        
        self.__middleSeparator3=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__middleSeparator3.grid(row = 3, column = 3,sticky=tk.E+tk.W)
        
        self.__middleSeparator4=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__middleSeparator4.grid(row = 3, column = 4,sticky=tk.E+tk.W)
        
        #separator that stretches over three rows, rowspan did not work
        self.__leftSeparator0=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__leftSeparator0.grid(row = 2, column = 1,sticky=tk.S+tk.N)
        self.__leftSeparator1=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__leftSeparator1.grid(row = 3, column = 1,sticky=tk.S+tk.N)
        self.__leftSeparator2=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__leftSeparator2.grid(row = 4, column = 1,sticky=tk.S+tk.N)
        
        self.__rightSeparator0=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__rightSeparator0.grid(row = 1, column = 3,sticky=tk.S+tk.N)
        self.__rightSeparator1=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__rightSeparator1.grid(row = 2, column = 3,sticky=tk.S+tk.N)
        self.__rightSeparator2=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__rightSeparator2.grid(row = 3, column = 3,sticky=tk.S+tk.N)
        self.__rightSeparator3=tk.Frame(self.__root,height=2,bd=1,relief=tk.SUNKEN)
        self.__rightSeparator3.grid(row = 4, column = 3,sticky=tk.S+tk.N)
        
        
        #button frame
        self.__buttonFrame=tk.Frame(self.__root,bg="white",width=self.__window_width/4,height=self.__window_height*2/6)
        self.__buttonFrame.grid(row = 4, column = 0)
        
        self.__startButton=tk.Button(self.__buttonFrame, text="start", width=8, command=self.startFunction,state=tk.DISABLED)
        self.__startButton.place(relx=0.25,rely=0.20,anchor=tk.CENTER)
        self.__buttonsToEnable.append(self.__startButton)
        self.__gloriaStarted=False
        
        self.__autoMotorButton=tk.Button(self.__buttonFrame, text="auto motor", width=8, command=self.enableAutoMotor,state=tk.DISABLED)
        self.__autoMotorButton.place(relx=0.75,rely=0.20,anchor=tk.CENTER)
        self.__buttonsToEnable.append(self.__autoMotorButton)
        
        self.__autoArmButton=tk.Button(self.__buttonFrame, text="auto arm", width=8, command=self.enableAutoArm,state=tk.DISABLED)
        self.__autoArmButton.place(relx=0.75,rely=0.50,anchor=tk.CENTER)
        self.__buttonsToEnable.append(self.__autoArmButton)
        
        self.__gotPackageButton=tk.Button(self.__buttonFrame, text="got package", width=8, command=self.gotPackage,state=tk.DISABLED)
        self.__gotPackageButton.place(relx=0.75,rely=0.80,anchor=tk.CENTER)
        self.__buttonsToEnable.append(self.__gotPackageButton)
        
        self.__calibrateTapeButton=tk.Button(self.__buttonFrame, text="calibrate tape", width=8, command=self.calibrateTape,state=tk.DISABLED)
        self.__calibrateTapeButton.place(relx=0.25,rely=0.50,anchor=tk.CENTER)
        self.__buttonsToEnable.append(self.__calibrateTapeButton)
        
        self.__calibrateFloorButton=tk.Button(self.__buttonFrame, text="calibrate floor", width=8, command=self.calibrateTape,state=tk.DISABLED)
        self.__calibrateFloorButton.place(relx=0.25,rely=0.80,anchor=tk.CENTER)
        self.__buttonsToEnable.append(self.__calibrateFloorButton)
        
        self.__overviewFrame=tk.Frame(self.__root,bg="white",width=self.__window_width*2/4,height=self.__window_height*2/6)
        self.__overviewFrame.grid(row = 2, column = 2)
        
        self.__overviewCanvas=tk.Canvas(self.__overviewFrame,width=self.__window_width*2/4,height=self.__window_height*2/6)
        self.__overviewCanvas.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        self.__root.update()
        self.__overviewRobot=self.__overviewCanvas.create_rectangle(int(self.__overviewCanvas.winfo_width()*0.40),int(self.__overviewCanvas.winfo_height()*0.20),int(self.__overviewCanvas.winfo_width()*0.60),int(self.__overviewCanvas.winfo_height()*0.80))
        self.__leftMiddleSensor=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4-30),int(self.__overviewCanvas.winfo_height()/2.0-4),int(self.__overviewCanvas.winfo_width()/2.0+4-30),int(self.__overviewCanvas.winfo_height()/2.0+4),fill="red")
        self.__rightMiddleSensor=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4+30),int(self.__overviewCanvas.winfo_height()/2.0-4),int(self.__overviewCanvas.winfo_width()/2.0+4+30),int(self.__overviewCanvas.winfo_height()/2.0+4),fill="red")
        self.__linesensorDots={}
        
        self.__linesensorDot0=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4-50),int(self.__overviewCanvas.winfo_height()/2.0-4-80),int(self.__overviewCanvas.winfo_width()/2.0+4-50),int(self.__overviewCanvas.winfo_height()/2.0+4-80),fill="red")
        self.__linesensorDots[0]=self.__linesensorDot0
        
        self.__linesensorDot1=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4-40),int(self.__overviewCanvas.winfo_height()/2.0-4-80),int(self.__overviewCanvas.winfo_width()/2.0+4-40),int(self.__overviewCanvas.winfo_height()/2.0+4-80),fill="red")
        self.__linesensorDots[1]=self.__linesensorDot1
        
        self.__linesensorDot2=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4-30),int(self.__overviewCanvas.winfo_height()/2.0-4-80),int(self.__overviewCanvas.winfo_width()/2.0+4-30),int(self.__overviewCanvas.winfo_height()/2.0+4-80),fill="red")
        self.__linesensorDots[2]=self.__linesensorDot2
        
        self.__linesensorDot3=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4-20),int(self.__overviewCanvas.winfo_height()/2.0-4-80),int(self.__overviewCanvas.winfo_width()/2.0+4-20),int(self.__overviewCanvas.winfo_height()/2.0+4-80),fill="red")
        self.__linesensorDots[3]=self.__linesensorDot3
        self.__linesensorDot4=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4-10),int(self.__overviewCanvas.winfo_height()/2.0-4-80),int(self.__overviewCanvas.winfo_width()/2.0+4-10),int(self.__overviewCanvas.winfo_height()/2.0+4-80),fill="red")
        self.__linesensorDots[4]=self.__linesensorDot4
        self.__linesensorDot5=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4-0),int(self.__overviewCanvas.winfo_height()/2.0-4-80),int(self.__overviewCanvas.winfo_width()/2.0+4-0),int(self.__overviewCanvas.winfo_height()/2.0+4-80),fill="red")
        self.__linesensorDots[5]=self.__linesensorDot5
        self.__linesensorDot6=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4+10),int(self.__overviewCanvas.winfo_height()/2.0-4-80),int(self.__overviewCanvas.winfo_width()/2.0+4+10),int(self.__overviewCanvas.winfo_height()/2.0+4-80),fill="red")
        self.__linesensorDots[6]=self.__linesensorDot6
        self.__linesensorDot7=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4+20),int(self.__overviewCanvas.winfo_height()/2.0-4-80),int(self.__overviewCanvas.winfo_width()/2.0+4+20),int(self.__overviewCanvas.winfo_height()/2.0+4-80),fill="red")
        self.__linesensorDots[7]=self.__linesensorDot7
        self.__linesensorDot8=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4+30),int(self.__overviewCanvas.winfo_height()/2.0-4-80),int(self.__overviewCanvas.winfo_width()/2.0+4+30),int(self.__overviewCanvas.winfo_height()/2.0+4-80),fill="red")
        self.__linesensorDots[8]=self.__linesensorDot8
        self.__linesensorDot9=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4+40),int(self.__overviewCanvas.winfo_height()/2.0-4-80),int(self.__overviewCanvas.winfo_width()/2.0+4+40),int(self.__overviewCanvas.winfo_height()/2.0+4-80),fill="red")
        self.__linesensorDots[9]=self.__linesensorDot9
        self.__linesensorDot10=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-4+50),int(self.__overviewCanvas.winfo_height()/2.0-4-80),int(self.__overviewCanvas.winfo_width()/2.0+4+50),int(self.__overviewCanvas.winfo_height()/2.0+4-80),fill="red")
        self.__linesensorDots[10]=self.__linesensorDot10
        
        self.__distanceLineLeft=self.__overviewCanvas.create_line(int(self.__overviewCanvas.winfo_width()/2.0-70),int(self.__overviewCanvas.winfo_height()/2.0-30),int(self.__overviewCanvas.winfo_width()/2.0-70),int(self.__overviewCanvas.winfo_height()/2.0+30),width=4,fill="black")
        self.__distanceLineRight=self.__overviewCanvas.create_line(int(self.__overviewCanvas.winfo_width()/2.0+70),int(self.__overviewCanvas.winfo_height()/2.0-30),int(self.__overviewCanvas.winfo_width()/2.0+70),int(self.__overviewCanvas.winfo_height()/2.0+30),width=4,fill="black")

        self.__overviewArmRing=self.__overviewCanvas.create_oval(int(self.__overviewCanvas.winfo_width()/2.0-10),int(self.__overviewCanvas.winfo_height()/2.0-10),int(self.__overviewCanvas.winfo_width()/2.0+10),int(self.__overviewCanvas.winfo_height()/2.0+10))
        self.__overviewArmHorizontalLine=self.__overviewCanvas.create_line(int(self.__overviewCanvas.winfo_width()/2.0-10),int(self.__overviewCanvas.winfo_height()/2.0),int(self.__overviewCanvas.winfo_width()/2.0+10),int(self.__overviewCanvas.winfo_height()/2.0),width=2,fill="black")
        self.__overviewArmVerticalLine=self.__overviewCanvas.create_line(int(self.__overviewCanvas.winfo_width()/2.0),int(self.__overviewCanvas.winfo_height()/2.0-10),int(self.__overviewCanvas.winfo_width()/2.0),int(self.__overviewCanvas.winfo_height()/2.0+10),width=2,fill="black")

        self.__overviewArmHeight=self.__overviewCanvas.create_rectangle(int(self.__overviewCanvas.winfo_width()*0.95-10),int(self.__overviewCanvas.winfo_height()*0.5),int(self.__overviewCanvas.winfo_width()*0.95+10),int(self.__overviewCanvas.winfo_height()-2))

        
        self.__speedFrame=tk.Frame(self.__root,bg="white",width=self.__window_width*2/4,height=self.__window_height*2/6)
        self.__speedFrame.grid(row = 4, column = 2)
        
        self.__speedCanvas=tk.Canvas(self.__speedFrame,width=self.__window_width*2/4,height=self.__window_height*2/6)
        self.__speedCanvas.place(relx=0.5,rely=0.5,anchor=tk.CENTER)
        self.__root.update()
        
        self.__leftSpeedBar=self.__speedCanvas.create_rectangle(int(self.__speedCanvas.winfo_width()*0.20),int(self.__speedCanvas.winfo_height()*0.50),int(self.__speedCanvas.winfo_width()*0.30),int(self.__speedCanvas.winfo_height()*0.55),fill="green")
        self.__rightSpeedBar=self.__speedCanvas.create_rectangle(int(self.__speedCanvas.winfo_width()*0.70),int(self.__speedCanvas.winfo_height()*0.50),int(self.__speedCanvas.winfo_width()*0.80),int(self.__speedCanvas.winfo_height()*0.55),fill="green")
        
        self.__regulatorFrame=tk.Frame(self.__root,bg="white",width=self.__window_width/4,height=self.__window_height*2/6)
        self.__regulatorFrame.grid(row = 2, column = 4)
        
        #regulatorplot
        f = Figure(figsize=(100,100), dpi=100,tight_layout=True)
        self.__regulatorPlotFrame=f.gca()
        self.__regulatorPlotFrame.axes.get_xaxis().set_ticks([])
        self.__regulatorPlotFrame.axes.get_yaxis().set_ticks([])
        self.__regulatorPlot = f.add_subplot(111)
        t = arange(0.0,3.0,0.01)
        s = sin(2*pi*t)
        self.__regulatorPlot.plot(t,s)
        
        self.__Regulatorcanvas = FigureCanvasTkAgg(f, master=self.__regulatorFrame)
        self.__Regulatorcanvas.show()
        self.__Regulatorcanvas.get_tk_widget().place(relwidth=1.0,relheight=1.0,relx=0.5,rely=0.5,anchor=tk.CENTER)
        
        
        self.__errorFrame=tk.Frame(self.__root,bg="white",width=self.__window_width/4,height=self.__window_height*2/6)
        self.__errorFrame.grid(row = 4, column = 4)
        self.__ErrorScrollbar = tk.Scrollbar(self.__errorFrame, orient=tk.VERTICAL)
        self.__errorListbox = tk.Listbox(self.__errorFrame, yscrollcommand=self.__ErrorScrollbar.set)
        self.__ErrorScrollbar.config(command=self.__errorListbox.yview)
        self.__errorListbox.place(relwidth=0.9,relheight=1,relx=0.46,rely=0.5,anchor=tk.CENTER)
        self.__ErrorScrollbar.place(relx=0.95,rely=0.5,anchor=tk.CENTER)
        
        self.__terminalFrame=tk.Frame(self.__root,bg="white",width=self.__window_width,height=self.__window_height/6)
        self.__terminalFrame.grid(row = 6, column = 0,columnspan=5)
        self.__terminalInfo = self.__terminalFrame.winfo_id()
        self.__characterWidth=str(int(self.__screenWidth/6))
        command="xterm -into %d -geometry  "+self.__characterWidth+"x40 -sb &"
        os.system(command % self.__terminalInfo)
        #starts mainloop
        self.__root.update()
        self.__root.after(2000, self.screenSaver)
        self.__root.after(50,self.peripheralUpdater)
        self.__root.after(100,self.sensorUpdater)
        self.__root.mainloop()
    def connectArmJoystick(self):
        temp=Joystick("arm")
        if temp.get_init():
            self.__armJoy=temp
            self.__connectArmJoystickButton.config(state=tk.DISABLED)
    def connectMotorJoystick(self):
        temp=Joystick("motor")
        if temp.get_init():
            self.__motorJoy=temp
            self.__connectMotorJoystickButton.config(state=tk.DISABLED)
    def insertError(self,error):
        self.__errorListbox.insert(tk.END,error)
        self.__errorListbox.yview(tk.END)
    def updateArmPosition(self,values):
        temp_list=[]
        temp_list.append(round(self.__overviewCanvas.winfo_width()/2.0-10+values[0]))
        temp_list.append(round(self.__overviewCanvas.winfo_height()/2.0-10-values[1]))
        temp_list.append(round(self.__overviewCanvas.winfo_width()/2.0+10+values[0]))
        temp_list.append(round(self.__overviewCanvas.winfo_height()/2.0+10-values[1]))
        self.__overviewCanvas.coords(self.__overviewArmRing,tuple(temp_list))
        temp_list=[]
        temp_list.append(round(self.__overviewCanvas.winfo_width()/2.0-10+values[0]))
        temp_list.append(round(self.__overviewCanvas.winfo_height()/2.0-values[1]))
        temp_list.append(round(self.__overviewCanvas.winfo_width()/2.0+10+values[0]))
        temp_list.append(round(self.__overviewCanvas.winfo_height()/2.0-values[1]))
        self.__overviewCanvas.coords(self.__overviewArmVerticalLine,tuple(temp_list))
        temp_list=[]
        temp_list.append(round(self.__overviewCanvas.winfo_width()/2.0+values[0]))
        temp_list.append(round(self.__overviewCanvas.winfo_height()/2.0-10-values[1]))
        temp_list.append(round(self.__overviewCanvas.winfo_width()/2.0+values[0]))
        temp_list.append(round(self.__overviewCanvas.winfo_height()/2.0+10-values[1]))
        self.__overviewCanvas.coords(self.__overviewArmHorizontalLine,tuple(temp_list))
        
        temp_list=self.__overviewCanvas.coords(self.__overviewArmHeight)
        
        temp_list[1]=round(self.__overviewCanvas.winfo_height()-values[2])
        self.__overviewCanvas.coords(self.__overviewArmHeight,tuple(temp_list))
        self.__root.update()
        
    def setMiddleSensor(self,left,right):
        if left>0.5:
            self.__overviewCanvas.itemconfig(self.__leftMiddleSensor, fill="green")
        else:
            self.__overviewCanvas.itemconfig(self.__leftMiddleSensor, fill="red")
        if right>0.5:
            self.__overviewCanvas.itemconfig(self.__rightMiddleSensor, fill="green")
        else:
            self.__overviewCanvas.itemconfig(self.__rightMiddleSensor, fill="red")
        self.__root.update()
    def DistanceSensorsTest(self):
        if not self.__gloria:
            for i in range(0,30):
                self.updateDistanceSensor(i, i)
                time.sleep(0.01)
            for i in range(30,0,-1):
                self.updateDistanceSensor(i, i)
                time.sleep(0.01)
    def updateDistanceSensor(self,right,left):
        temp_list=self.__overviewCanvas.coords(self.__distanceLineLeft)
        temp_list[0]=temp_list[2]=round(self.__overviewCanvas.winfo_width()/2.0-70-(30-left))
        self.__overviewCanvas.coords(self.__distanceLineLeft,tuple(temp_list))
        
        temp_list=self.__overviewCanvas.coords(self.__distanceLineRight)
        temp_list[0]=temp_list[2]=round(self.__overviewCanvas.winfo_width()/2.0+70+(30-right))
        self.__overviewCanvas.coords(self.__distanceLineRight,tuple(temp_list))
        self.__root.update()
    def speedBarsTester(self):
        if not self.__gloria:
            for i in range(-100,100):
                self.setSpeedbars(i, i)
                time.sleep(0.001)
            for i in range(100,0,-1):
                self.setSpeedbars(i, i)
                time.sleep(0.001)
    def updateRegulatorError(self,error):
        self.__oldRegulatorErrors[self.__oldRegulatorCounter]=error[0]
        self.__oldRegulatorCounter=self.__oldRegulatorCounter+1
        if self.__oldRegulatorCounter>99:
            self.__oldRegulatorCounter=0
        self.updateRegulatorgraph()
    def updateRegulatorgraph(self):
        self.__regulatorPlot.cla()
        self.__regulatorPlot.plot(np.array(self.__oldRegulatorTime,dtype=float),np.array(self.__oldRegulatorErrors,dtype=float))
        self.__regulatorPlotFrame.axes.get_xaxis().set_ticks([])
        self.__regulatorPlotFrame.axes.get_yaxis().set_ticks([])
        self.__Regulatorcanvas.show()
    def regulatorGraphTest(self):
        if not self.__gloria:
            self.__regulatorPlot.cla()
            for i in range(100):
                t = arange(0.0,3.0,0.01)
                s = sin(2*pi*t)
                self.__regulatorPlot.scatter(t[i],s[i])
                time.sleep(0.0001)
                self.__regulatorPlotFrame.axes.get_xaxis().set_ticks([])
                self.__regulatorPlotFrame.axes.get_yaxis().set_ticks([])
                self.__Regulatorcanvas.show()
            
    def updateSpeedFromJoystick(self):
        x=self.__motorJoy.x_axis()
        y=self.__motorJoy.y_axis()
        z=math.sqrt(x*x+y*y)
        if z!=0.0:
            rad = math.acos(abs(x)/z)
        else:
            rad=0.0
        angle = rad*180/math.pi
        tcoeff = -1 + (angle/90)*2
        turn = tcoeff * abs(abs(y) - abs(x))
        turn = round(turn*100)/100
        move = max(abs(y),abs(x))
        if( (x >= 0 and y >= 0) or (x < 0 and  y < 0) ):
            right = move
            left = turn
        else:
            left = move
            right = turn
        if(y < 0):
            right = 0 - right
            left = 0 - left
        left=-int(left*100)
        right=-int(right*100)
        if self.__gloria:
            try:
                self.__gloria.setMotorSpeed(left,right)
            except (socket.error,AttributeError):
                self.handleInternalErrors("broken connection")
        self.setSpeedbars(left, right)
    def updateArmFromJoystick(self):
        self.__gloria.updateSensors()
        armPosition=self.__gloria.getArmPosition()
        x=int(self.__armJoy.x_axis()*4.0+armPosition[0])
        y=int(-self.__armJoy.y_axis()*4.0+armPosition[1])
        z=int(self.__armJoy.z_axis()*4.0+armPosition[2])
        
        self.__gloria.setArmPosition(x, y, z, int(self.__armJoy.axis2()*90),int( -90 +self.__armJoy.axis3()*150), int(70+self.__armJoy.axis4()*70))
    def linesensorBarsTester(self):
        if not self.__gloria:
            test_data=[[0,0,0,0,0,0,0,0,0,0,0],[128,0,0,0,0,0,0,0,0,0,0],[256,128,0,0,0,0,0,0,0,0,0],[512,256,128,0,0,0,0,0,0,0,0],[1024,512,256,128,0,0,0,0,0,0,0],
                       [512,1024,512,256,128,0,0,0,0,0,0],[256,512,1024,512,256,128,0,0,0,0,0],[128,256,512,1024,512,256,128,0,0,0,0],[0,128,256,512,1024,512,256,128,0,0,0],[0,0,128,256,512,1024,512,256,128,0,0]
                       ,[0,0,0,128,256,512,1024,512,256,128,0],[0,0,0,0,128,256,512,1024,512,256,128],[0,0,0,0,0,128,256,512,1024,512,256],[0,0,0,0,0,0,128,256,512,1024,512],[0,0,0,0,0,0,0,128,256,512,1024],[0,0,0,0,0,0,0,0,128,256,512],[0,0,0,0,0,0,0,0,0,128,256],[0,0,0,0,0,0,0,0,0,0,128],[0,0,0,0,0,0,0,0,0,0,0]]
            for i in range(len(test_data)):
                self.updateLinesensor([e/1024.0 for e in test_data[i]])
                self.__root.update()
                time.sleep(0.1)
    def screenSaver(self):
        if self.__screenSaver and not self.__gloria:
            self.linesensorBarsTester()
            self.speedBarsTester()
            self.regulatorGraphTest()
            self.DistanceSensorsTest()
        self.__root.after(1000, self.screenSaver)
        
    def peripheralUpdater(self):
        if self.__motorJoy:
            self.updateSpeedFromJoystick()
        if self.__armJoy and self.__gloria:
            try:
                self.updateArmFromJoystick()
            except (socket.error,AttributeError):
                self.handleInternalErrors("broken connection")
        self.__root.after(50,self.peripheralUpdater)
    def sensorUpdater(self):
        if self.__gloria:
            print(self.__gloria.getSensorList())
            try:
                self.__gloria.updateSensors()
            except (socket.error,AttributeError):
                self.handleInternalErrors("broken connection")
            try:
                self.updateArmPosition(self.__gloria.getArmPosition())
            except (socket.error,AttributeError):
                self.handleInternalErrors("broken connection")
            try:
                self.updateRegulatorError(self.__gloria.getRegulatorError())
            except (socket.error,AttributeError):
                self.handleInternalErrors("broken connection")
            try:
                self.updateDistanceSensor(self.__gloria.getLeftDistanceSensor(), self.__gloria.getRightDistanceSensor())
            except (socket.error,AttributeError):
                self.handleInternalErrors("broken connection")
            try:
                self.updateLinesensor(self.__gloria.getLineSensor())
            except (socket.error,AttributeError):
                self.handleInternalErrors("broken connection")
            try:
                tempList=self.__gloria.getErrorCodes()
                for element in tempList:
                    self.insertError(element)
                #todo implement clearErrors on gloria
            except (socket.error,AttributeError):
                self.handleInternalErrors("broken connection")
        self.__root.after(100,self.sensorUpdater)
    def calibrateTape(self):
        #toto implement command for tape calibration on gloria
        pass
    def calibrateFloor(self):
        #toto implement command for floor calibration on gloria
        pass
    def setSpeedbars(self,left,right):
        temp_list=self.__speedCanvas.coords(self.__leftSpeedBar)
        if left>0:
            temp_list[3]=round(self.__speedCanvas.winfo_height()*0.50)-round((self.__speedCanvas.winfo_height()*0.50)*left/100)
            temp_list[1]=round(self.__speedCanvas.winfo_height()*0.50)
        else:
            temp_list[1]=round(self.__speedCanvas.winfo_height()*0.50)-round((self.__speedCanvas.winfo_height()*0.50)*left/100)
            temp_list[3]=round(self.__speedCanvas.winfo_height()*0.50)
        self.__speedCanvas.coords(self.__leftSpeedBar,tuple(temp_list))
        if left>0:
            self.__speedCanvas.itemconfig(self.__leftSpeedBar, fill="green")
        else:
            self.__speedCanvas.itemconfig(self.__leftSpeedBar, fill="red")
            
        temp_list=self.__speedCanvas.coords(self.__rightSpeedBar)
        if right>0:
            temp_list[3]=round(self.__speedCanvas.winfo_height()*0.50)-round((self.__speedCanvas.winfo_height()*0.50)*right/100)
            temp_list[1]=round(self.__speedCanvas.winfo_height()*0.50)
        else:
            temp_list[1]=round(self.__speedCanvas.winfo_height()*0.50)-round((self.__speedCanvas.winfo_height()*0.50)*right/100)
            temp_list[3]=round(self.__speedCanvas.winfo_height()*0.50)
            
        self.__speedCanvas.coords(self.__rightSpeedBar,tuple(temp_list))
        if right>0:
            self.__speedCanvas.itemconfig(self.__rightSpeedBar, fill="green")
        else:
            self.__speedCanvas.itemconfig(self.__rightSpeedBar, fill="red")

        self.__root.update()
        
        
    def gotPackage(self):
        try:
            self.__gloria.setPackageTrue()
        except (socket.error,AttributeError):
                self.handleInternalErrors("broken connection")
    def enableAutoMotor(self):
        try:
            self.__gloria.setAutoMotor(True)
        except (socket.error,AttributeError):
                self.handleInternalErrors("broken connection")
        self.__autoMotorButton.config(text="man motor")
        self.__autoMotorButton.config(command=self.disableAutoMotor)
    def disableAutoMotor(self):
        try:
            self.__gloria.setAutoMotor(False)
        except (socket.error,AttributeError):
            self.handleInternalErrors("broken connection")
        self.__autoMotorButton.config(text="auto motor")
        self.__autoMotorButton.config(command=self.enableAutoMotor)
    def enableAutoArm(self):
        try:
            self.__gloria.setAutoArm(True)
        except (socket.error,AttributeError):
            self.handleInternalErrors("broken connection")
        self.__autoArmButton.config(text="man arm")
        self.__autoArmButton.config(command=self.disableAutoArm)
    def disableAutoArm(self):
        try:
            self.__gloria.setAutoArm(False)
        except (socket.error,AttributeError):
            self.handleInternalErrors("broken connection")
        self.__autoArmButton.config(text="auto arm")
        self.__autoArmButton.config(command=self.enableAutoArm)
        
    def startFunction(self):
        if not self.__gloriaStarted:
            self.__startButton.config(text="stop")
            try:
                self.__gloria.start()
            except (socket.error,AttributeError):
                self.handleInternalErrors("broken connection")
            self.__gloriaStarted=True
        else:
            self.__startButton.config(text="start")
            try:
                self.__gloria.stop()
            except (socket.error,AttributeError):
                self.handleInternalErrors("broken connection")
            self.__gloriaStarted=False
    def updateLinesensor(self,values):
        for i in range(11):
            if values[i]>0.5:
                self.__overviewCanvas.itemconfig(self.__linesensorDots[i], fill="green")
            else:
                self.__overviewCanvas.itemconfig(self.__linesensorDots[i], fill="red")
            
        for i in range(11):
            values[i]=int(abs(float(values[i])*1023))
        for i in range(11):
            temp_list=self.__linesensorCanvas.coords(self.__bars[i])
            temp_list[1]=round(self.__window_height/6-(float(values[i])/1024.0)*self.__window_height/6)
            self.__linesensorCanvas.coords(self.__bars[i],tuple(temp_list))
            self.__root.update()
    def openConfigFile(self):
        try:
            config_file = open("config.txt", "r")
            self.__ip_adress=config_file.read()
            config_file.close()
        except IOError,e:
            self.__ip_adress="0.0.0.0"
            config_file = open("config.txt", "w")
            config_file.write(self.__ip_adress)
            config_file.close()
    def connectFunction(self):
        ip_adress=self.__ip_entry.get()
        valid=True
        try:
            socket.inet_aton(ip_adress)
            self.__ip_adress=ip_adress
            config_file=open("config.txt", "w")
            config_file.truncate()
            config_file.write(self.__ip_adress)
            config_file.close()
        except (socket.error,AttributeError):
            self.handleInternalErrors("invalid ip")
            valid=False
        if valid:
            try:
                self.__gloria=pcModule.pcModule(self.__ip_adress)
                self.enableButtons(True)
                self.__screenSaver=False
                self.__connect_button.config(state=tk.DISABLED)
            except socket.error:
                self.handleInternalErrors("connection refused")
    def enableButtons(self,value):
        if value:
            for element in self.__buttonsToEnable:
                element.config(state=tk.NORMAL)
        else:
            for element in self.__buttonsToEnable:
                element.config(state=tk.DISABLED)
        
        
    def handleInternalErrors(self,error):
        self.insertError(error)
        if error=="broken connection":
            self.__gloria=None
            self.enableButtons(False)
            self.__screenSaver=True
            self.__connect_button.config(state=tk.NORMAL)
        
        
temp=Gui()
