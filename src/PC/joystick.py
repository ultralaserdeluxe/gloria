import pygame
import math
import time
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

    def getMotorSpeed(self):
	x=-self.x_axis()
	y=-self.y_axis()
	z = math.sqrt(x*x + y*y)	
	if z!=0.0:
    		rad = math.acos(abs(x)/z)
	else:
		rad=math.pi/2.0
    	angle = rad*180/math.pi
    	tcoeff = -1 + (angle/90)*2
    	turn = tcoeff * abs(abs(y) - abs(x))
    	turn = round(turn*100)/100;
    	move = max(abs(y),abs(x));
    	if( (x >= 0 and y >= 0) or (x < 0 and  y < 0) ):
        	right = move;
        	left = turn;
 	else: 
        	left = move;
        	right = turn;
    	if(y < 0):
        	right = 0 - right;
        	left = 0 - left;
	return [left*255,right*255]
