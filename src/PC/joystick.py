import pygame
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
#joystick=Joystick()
##while True:
 #   print(joystick.x_axis())
 #   print(joystick.y_axis())
 #   print(" ")