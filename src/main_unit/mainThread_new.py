import sys
import time
import Queue
import logging as log

import pcThread
import regulator
import driveUnit
import sensorThread

HALTED = "HALTED"
MANUAL = "MANUAL"
LINE = "LINE"

class Station:
    def __init__(self, empty, left):
        self.empty = empty
        self.left = left

    def is_empty(self):
        return self.empty

    def is_full(self):
        return not self.empty

    def is_left(self):
        return self.left

    def is_right(self):
        return not self.left

class Gloria:
    def __init__(self, shared_stuff, cmd_queue):
        self.shared_stuff = shared_stuff
        self.cmd_queue = cmd_queue

        self.drive = driveUnit.driveUnit()
        self.current_speed = [None, None]

        self.state = None
        self.has_package = False
        self.station_queue = []

    def get_command(self):
        if not self.cmd_queue.empty():
            _cmd = self.cmd_queue.get()
            cmd = _cmd[0]
            args = _cmd[1:]
            if args:
                args = _cmd[1]
            log.debug("Got command \"%s\" and args %s." %(cmd, str(args)))
            return cmd, args
        return "", []

    def change_state(self, new_state):
        log.info("Changing state from %s to %s." %(self.state, new_state))        
        self.state = new_state

    def handle_command(self, cmd, args):
        if cmd == "start" and self.state == HALTED:
            self.change_state(MANUAL)
        elif cmd == "halt" and self.state != HALTED:
            self.change_state(HALTED)
        elif cmd == "autoMotor" and args == True and self.state == MANUAL:
            self.change_state(LINE)
        elif cmd == "autoMotor" and args == False and self.state == LINE:
            self.set_speed(0, 0)
            self.change_state(MANUAL)
        elif cmd == "":
            pass

    def run(self):
        self.change_state(HALTED)

        while True:
            time.sleep(0.005)
            cmd, args = self.get_command()
            self.handle_command(cmd, args)

            # State execution
            if self.state == HALTED:
                self.halted()
            elif self.state == MANUAL:
                self.manual(cmd, args)
            elif self.state == LINE:
                self.line()
            else:
                log.critical("Vegetable state! state=\"%s\"" %str(self.state))
                sys.exit(1)

    def halted(self):
        self.set_speed(0, 0)

    def manual(self, cmd, args):
        if cmd == "calibrateFloor":
            #TODO: Handle calibrate floor            
            pass
        elif cmd == "calibrateTape":
            #TODO: Handle calibrate tape
            pass
        elif cmd == "motorSpeed":
            self.set_speed(args[0], args[1])
        elif cmd == "armPosition":
            self.steer_arm(*args)

    def line(self):
        # Regulate
        left, right = shared_stuff["regulator"]
        self.set_speed(left, right)

    def set_speed(self, left, right):
        if left != self.current_speed[0] or right != self.current_speed[1]:
            log.debug("set_speed: left=%d right=%d" %(left, right))

            self.current_speed[0] = left
            self.current_speed[1] = right

            self.drive.setMotorLeft(left)
            self.drive.setMotorRight(right)
            self.drive.sendAllMotor()

    def steer_arm(self, x, y, z, p, w, g):
        log.debug("steer_arm: x=%d y=%d z=%d p=%d w=%d g=%d" %(x, y, z, p, w, g))

        arm.setAll([x, y, z, p, w, g])
        servo_values = arm.getServoValues()
        
        for i in range(6):
            drive.setArmAxis(i+1, servo_values[i])
            time.sleep(0.001)
            drive.sendAllAxis()
            time.sleep(0.001)

if __name__ == "__main__":
    line_cal_max = [213, 206, 232, 180, 232, 174, 237, 183, 199, 177, 178]
    line_cal_min = [75, 97, 126, 61, 147, 39, 154, 57, 80, 63, 50]

    shared_stuff = {"lineSensor" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "lineCalMax" : line_cal_max,
                    "lineCalMin" : line_cal_min,
                    "middleSensor" : [0, 0],
                    "distance" :  [0, 0],
                    "armPosition" : [0, 0, 255, 4, 5, 5],
                    "errorCodes" : ["YngveProgrammedMeWrong"],
                    "motorSpeed" : [70, 70],
                    "latestCalibration" : "0000-00-00-15:00",
                    "autoMotor" : False,
                    "autoArm" : False,
                    "regulator" : [0, 0],
                    "error" : 0}

    sensor_thread = sensorThread.sensorThread(shared_stuff)
    sensor_thread.daemon=True
    sensor_thread.start()

    cmd_queue = Queue.Queue()
    pc_thread = pcThread.pcThread(cmd_queue, shared_stuff)
    pc_thread.daemon=True
    pc_thread.start()

    regulator = regulator.Regulator(shared_stuff)
    regulator.daemon=True
    regulator.start()

    log.basicConfig(level=log.DEBUG)
    gloria = Gloria(shared_stuff, cmd_queue)
    gloria.run()
