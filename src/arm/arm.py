from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pygame
from math import atan2,sqrt
class Arm():     
    def __init__(self):
        SEGMENTS = int(4) #number joints
        self.l = np.array([0, 150, 152, 62])# length of sections
        self.w = np.array([0]*SEGMENTS,dtype=float) #horizontal coordinate
        self.z = np.array([0]*SEGMENTS,dtype=float) #vertical coordinate
        self.x = np.array([0]*SEGMENTS,dtype=float) #x axis components
        self.y = np.array([0]*SEGMENTS,dtype=float) #y axis components
        self.a = np.array([np.pi]*SEGMENTS,dtype=float) #angle for the link, reference is previous link
        #todo rewrite gripper angle
        self.gripper_angle = np.array([90])
        self.tw = 0.0 # w axis position depth
        self.tz = 0.0 # z axis starting position height
        self.l12 = 0.0 # hypotenuse belween a1 & a2
        self.a12 = 0.0 #inscribed angle between hypotenuse, w   
        
    def calc_p2(self):#calculates position 2
        self.w[3] = self.tw
        self.z[3] = self.tz
        self.w[2] = self.tw-np.cos(np.radians(self.gripper_angle[0]))*self.l[3]
        self.z[2] = self.tz-np.sin(np.radians(self.gripper_angle[0]))*self.l[3]
        self.l12 = np.sqrt(np.square(self.w[2])+np.square(self.z[2]))
        
    def calc_p1(self):#calculate position 1
        self.a12 = np.arctan2(self.z[2],self.w[2])#return the appropriate quadrant 
        self.a[1] = np.arccos((np.square(self.l[1])+np.square(self.l12)-np.square(self.l[2]))
                              /(2*self.l[1]*self.l12))+self.a12
        self.w[1] = np.cos(self.a[1])*self.l[1]
        self.z[1] = np.sin(self.a[1])*self.l[1]
        
    def calc_x_y(self):#calc x_y Pcoordinates
        for i in range(len(self.x)):
            self.x[i] = self.w[i]*np.cos(self.a[0])
            self.y[i] = self.w[i]*np.sin(self.a[0])
        
    def get_angles(self): #get all of the motor angles see diagram
        self.a[2] = np.arctan((self.z[2]-self.z[1])/(self.w[2]-self.w[1]))-self.a[1]
        self.a[3] = np.deg2rad(self.gripper_angle[0])-self.a[1]-self.a[2] 
        angles = np.array(self.a).tolist()
        return angles
    
class Joystick():
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
    def x_axis(self):
        pygame.event.pump()
        return self.joystick.get_axis(0)
    def y_axis(self):
        pygame.event.pump()
        return self.joystick.get_axis(1)
    def throttle(self):
        pygame.event.pump()
        return self.joystick.get_axis(2)
    def z_axis(self):
        pygame.event.pump()
        return self.joystick.get_axis(3)
    
class Simulator():
    def __init__(self,arm):
        self.arm=arm
        self.closed=False
        self.joystick=Joystick()
        self.fig = plt.figure("Glorious Gloria")  #create the frame   
        self.ax = plt.axes([0.0, 0., 0.99, 0.99], projection='3d') #3d ax panel
        self.axe = plt.axes([0.25, 0.85, 0.001, .001])#panel for error message
        self.xyz=[0.0,0.0,0.0]
        self.display_error()#draw the error and hide it
        self.draw_robot()#draw function to draw robot
        def update_a0_joy(): 
            self.arm.a[0] =atan2(self.xyz[1],self.xyz[0])
        def update_tw_joy():#extension w Slider Event
            self.arm.tw = sqrt((self.xyz[1])**2 +(self.xyz[0])**2)
        def update_z_joy():#height z slider event
            self.arm.tz = self.xyz[2]
        def update_gripper():
            self.arm.gripper_angle[0]=90.0*self.joystick.throttle()
        def handle_close(evt):
            self.closed=True
        def update_joystick():
            self.xyz[0]=self.xyz[0]+self.joystick.x_axis()*8
            self.xyz[1]=self.xyz[1]+self.joystick.y_axis()*8
            self.xyz[2]=self.xyz[2]+self.joystick.z_axis()*8
        plt.ion()
        plt.show()
        self.fig.canvas.mpl_connect('close_event', handle_close)  
        while not self.closed:
            self.draw_robot()
            plt.pause(0.0001)
            update_joystick()
            update_a0_joy()
            update_tw_joy()
            update_z_joy()
            update_gripper()
    def display_error(self):
        self.axe.set_visible(False)
        self.axe.set_yticks([])
        self.axe.set_xticks([])
        self.axe.set_navigate(False)
        self.axe.text(0, 0, 'Arm Can Not Reach the Target!', style='oblique',
                      bbox={'facecolor':'red', 'alpha':0.5, 'pad':10}, size=20, va = 'baseline') 
    def draw_robot(self):#draw and update the 3D panel
        self.arm.calc_p2()
        self.arm.calc_p1()
        self.arm.calc_x_y()
        if self.arm.l12 < (self.arm.l[1]+self.arm.l[2]):#check boundaries
            self.axe.set_visible(False)#turn off error message panel
            self.set_positions()
            self.set_ax()
            print np.around(np.rad2deg(self.arm.get_angles()),2)
        else:
            self.axe.set_visible(True)#display error message panel
        plt.draw()
        
    def set_positions(self):#gets the x,y,z values for the line.
        #convert arrays to lists for drawing the line
        xs = np.array(self.arm.x).tolist()# = (self.z[0], self.z[1], self.z[2], self.z[3])
        ys = np.array(self.arm.y).tolist()
        zs = np.array(self.arm.z).tolist()
        self.ax.cla() #clear current axis
        #draw new lines,  two lines for "fancy" looks
        self.ax.plot(xs, ys, zs, 'o-', markersize=20,
                     markerfacecolor="orange", linewidth = 8, color="blue")
        self.ax.plot(xs, ys, zs, 'o-', markersize=4,
                     markerfacecolor="blue", linewidth = 1, color="silver")
        
    def set_ax(self):#ax panel set up
        self.ax.set_xlim3d(-200, 200)
        self.ax.set_ylim3d(-200, 200)
        self.ax.set_zlim3d(-5, 200)
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        for j in self.ax.get_xticklabels() + self.ax.get_yticklabels(): #hide ticks
            j.set_visible(False)
        self.ax.set_axisbelow(True) #send grid lines to the background
robot=Arm()
world=Simulator(robot)