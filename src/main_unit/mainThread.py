import sys
import time
import Queue
import logging as log

import pcThread
import regulator
import driveUnit
import sensorThread
import station_functions as se
import arm

HALTED = "HALTED"
MANUAL = "MANUAL"
LINE = "LINE"
STATION_FRONT = "STATION_FRONT"
STATION_CENTER = "STATION_CENTER"
STATION_BOTH = "STATION_BOTH"

class Station:
    number = 0

    def __init__(self, empty, left, number):
        self.empty = empty
        self.left = left
        self.number = number

    def is_empty(self):
        return self.empty

    def is_full(self):
        return not self.empty

    def is_left(self):
        return self.left

    def is_right(self):
        return not self.left

    def __str__(self):
        return "(number=%s, left=%s, empty=%s)" %(str(self.number), str(self.left), str(self.empty))

    @classmethod
    def create(cls, side, package):
        cls.number += 1
        log.debug("Station.create side=%s package=%s number=%s" %(side, package, str(cls.number)))
        station = None

        if side == se.LEFT and package == se.LEFT:
            station = Station(False, True, cls.number)
        elif side == se.LEFT and package != se.LEFT:
            station = Station(True, True, cls.number)
        elif side == se.RIGHT and package == se.RIGHT:
            station = Station(False, False, cls.number)
        elif side == se.RIGHT and package != se.RIGHT:
            station = Station(True, False, cls.number)
        else:
            log.critical("Tried to create Station with side=\"%s\" and package=\"%s\"!" %(side, package))

        log.debug("Created Station (%s) with empty=%s and left=%s." %(str(station.number), str(station.is_empty()), str(station.is_left())))
        return station

class Gloria:
    def __init__(self, shared_stuff, cmd_queue, sensor_thread):
        self.shared = shared_stuff
        self.cmd_queue = cmd_queue

        self.arm = arm.robotArm(self.shared)
        self.drive = driveUnit.driveUnit()
        self.current_speed = [None, None]
        self.linedet = se.LineDetector()

        self.state = None
        self.stored_state = None
        self.has_package = self.shared["hasPackage"] = False
        self.station_queue = []

        self.flush_timer = time.time()

        self.arm_return_pos = None
        self.carry_pos = (0, 100, 130, 0, 150, 140)

    def get_command(self):
        if not self.cmd_queue.empty():
            _cmd = self.cmd_queue.get()
            cmd = _cmd[0]
            args = _cmd[1:]
            if args:
                args = _cmd[1]
            if not cmd == "clearErrors":
                log.debug("Got command \"%s\" and args %s." %(cmd, str(args)))
            return cmd, args
        return "", []

    def change_state(self, new_state):
        if new_state == MANUAL:
            self.flush_command_queue()
        log.info("Changing state from %s to %s." %(self.state, new_state))
        self.shared["state"] = new_state
        self.state = new_state

    def store_state(self, state = None):
        if state is None: state = self.state
        log.info("Storing state: %s" %state)
        self.stored_state = state

    def restore_state(self):
        log.info("Restoring state from %s to %s" %(self.state, self.stored_state))
        self.refresh_flush_timer()
        self.change_state(self.stored_state)

    def handle_command(self, cmd, args):
        if cmd == "start" and self.state == HALTED:
            self.change_state(MANUAL)
        elif cmd == "halt" and self.state != HALTED:
            self.change_state(HALTED)
        elif cmd == "autoMotor" and args == True and self.state == MANUAL:
            self.refresh_flush_timer()
            self.change_state(LINE)
        elif cmd == "autoMotor" and args == False and self.state == LINE:
            self.set_speed(0, 0)
            self.change_state(MANUAL)
        elif cmd == "hasPackage" and args == True and self.state == MANUAL and self.stored_state != None:
	    log.info("Setting has_package to True.")

            self.has_package = self.shared["hasPackage"] = True
            self.arm_return_pos = self.shared["armPosition"][:]

            self.return_to_carry_position()

            self.restore_state()
        elif cmd == "clearErrors":
            self.shared["errorCodes"] = []
	elif cmd == "hasPackage" and args == False and self.state == MANUAL:
	    log.info("Setting has_package to False.")
            self.has_package = self.shared["hasPackage"] = False
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
            elif self.state == STATION_FRONT:
                self.station_front()
            elif self.state == STATION_CENTER:
                self.station_center()
            elif self.state == STATION_BOTH:
                self.station_both()
            else:
                log.critical("Vegetable state! state=\"%s\"" %str(self.state))
                sys.exit(1)

    def halted(self):
        self.shared["autoMotor"] = False
        self.stored_state = None
        self.has_package = self.shared["hasPackage"] = False
        self.station_queue = []
        self.set_speed(0, 0)

    def manual(self, cmd, args):
        self.shared["autoMotor"] = False

        if cmd == "calibrateFloor":
            sensor_thread.calibrateFloor()
            save_cal_to_file(self.shared)
        elif cmd == "calibrateTape":
            sensor_thread.calibrateTape()
            save_cal_to_file(self.shared)
        elif cmd == "motorSpeed":
            self.set_speed(args[0], args[1])
        elif cmd == "armPosition":
            self.steer_arm(*args)

    def line(self):
        self.shared["autoMotor"] = True

        if self.should_flush() and self.station_queue:
            self.flush_station_queue()
            return

        self.regulate()

        package = se.detect_package(*self.shared["distance"])

        front_values = self.shared["lineSensor"][:]
        center_values = self.shared["middleSensor"][:]

        self.linedet.add_values(front_values, center_values)

        front_station = self.linedet.station_front()
        center_station = self.linedet.station_center()

        if front_station != se.NO_STATION:
            front_obj = Station.create(front_station, package)
            log.info("Found front station with empty=%s and left=%s." %(str(front_obj.is_empty()), str(front_obj.is_left())))
            self.station_queue.append(front_obj)
            log.info([str(e) for e in self.station_queue])
            self.change_state(STATION_FRONT)
        elif center_station != se.NO_STATION:
            self.handle_center_station()

    def handle_center_station(self, next_state=STATION_CENTER):
        if self.is_on_stop() and not self.has_package:
            self.change_state(HALTED)
            return

        if len(self.station_queue) == 0:
            log.error("Found unknown center station!")
            self.change_state(next_state)
            return

        current_center = self.station_queue.pop(0)
        if self.has_package and not current_center.is_full():
            log.info("Current station (left=%s) has no package but robot does. Put down!" %current_center.is_left())
            log.info([str(e) for e in self.station_queue])
            self.put_down_package(current_center)
            self.change_state(next_state)
        elif not self.has_package and current_center.is_full():
            log.info("Current station (left=%s) has package and robot does not. Pick up!" %current_center.is_left())
            log.info([str(e) for e in self.station_queue])
            self.set_speed(0, 0)
            self.store_state(next_state)
            self.change_state(MANUAL)
        else:
            log.info("Current station (left=%s) package == robot package. Move on." %current_center.is_left())
            log.info([str(e) for e in self.station_queue])
            self.change_state(next_state)

    def station_front(self):
        self.shared["autoMotor"] = True

        self.regulate()

        front_values = self.shared["lineSensor"][:]
        center_values = self.shared["middleSensor"][:]

        self.linedet.add_values(front_values, center_values)

        front_station = self.linedet.station_front()
        center_station = self.linedet.station_center()

        if front_station == se.NO_STATION:
            log.info("Leaving front station.")
            self.refresh_flush_timer()
            self.change_state(LINE)
        elif center_station != se.NO_STATION:
            log.info("Detected center station while on front station.")
            self.handle_center_station(next_state=STATION_BOTH)

    def station_center(self):
        self.shared["autoMotor"] = True

        self.regulate()

        package = se.detect_package(*self.shared["distance"])

        front_values = self.shared["lineSensor"][:]
        center_values = self.shared["middleSensor"][:]

        self.linedet.add_values(front_values, center_values)

        front_station = self.linedet.station_front()
        center_station = self.linedet.station_center()

        if center_station == se.NO_STATION:
            log.info("Leaving center station.")
            self.refresh_flush_timer()
            self.change_state(LINE)
        elif front_station != se.NO_STATION:
            front_obj = Station.create(front_station, package)
            log.info("Found front station with empty=%s and left=%s." %(str(front_obj.is_empty()), str(front_obj.is_left())))
            self.station_queue.append(front_obj)
            log.info([str(e) for e in self.station_queue])
            self.change_state(STATION_BOTH)

    def station_both(self):
        self.shared["autoMotor"] = True

        self.regulate()

        front_values = self.shared["lineSensor"][:]
        center_values = self.shared["middleSensor"][:]

        self.linedet.add_values(front_values, center_values)

        front_station = self.linedet.station_front()
        center_station = self.linedet.station_center()

        if front_station != se.NO_STATION:
            log.info("Leaving front station.")
            self.change_state(STATION_CENTER)
        elif center_station != se.NO_STATION:
            log.info("Leaving center station.")
            self.change_state(STATION_FRONT)

    def regulate(self):
        left, right = self.shared["regulator"]
        self.set_speed(left, right)

    def steer_arm_fixed(self, x=None, y=None, z=None, p=None, w=None, g=None):
        if x is None:
            x = self.shared["armPosition"][0]
        if y is None:
            y = self.shared["armPosition"][1]
        if z is None:
            z = self.shared["armPosition"][2]
        if p is None:
            p = self.shared["armPosition"][3]
        if w is None:
            w = self.shared["armPosition"][4]
        if g is None:
            g = self.shared["armPosition"][5]

        old_position = tuple(self.shared["armPosition"])

        self.shared["armPosition"][0] = x
        self.shared["armPosition"][1] = y
        self.shared["armPosition"][2] = z
        self.shared["armPosition"][3] = p
        self.shared["armPosition"][4] = w
        self.shared["armPosition"][5] = g

        log.info("steer_arm: x=%d y=%d z=%d p=%d w=%d g=%d"
                 %(self.shared["armPosition"][0],
                   self.shared["armPosition"][1],
                   self.shared["armPosition"][2],
                   self.shared["armPosition"][3],
                   self.shared["armPosition"][4],
                   self.shared["armPosition"][5]))

        self.arm.setAll(self.shared["armPosition"])
        servo_values = self.arm.getServoValues()

        if self.arm.is_out_of_bounds():
            log.warning("Arm is out of bounds! Resetting to last good coordinates.")
            self.shared["armPosition"][0] = old_position[0]
            self.shared["armPosition"][1] = old_position[1]
            self.shared["armPosition"][2] = old_position[2]
            self.shared["armPosition"][3] = old_position[3]
            self.shared["armPosition"][4] = old_position[4]
            self.shared["armPosition"][5] = old_position[5]
        else:
            for i in range(6):
                self.drive.setArmAxis(i+1, servo_values[i])
                time.sleep(0.001)
                self.drive.sendAllAxis()
                time.sleep(0.001)

    def return_to_default_position(self):
        self.steer_arm_fixed(z=self.carry_pos[2], w=self.carry_pos[4], p=self.carry_pos[0], g=self.carry_pos[1])
        time.sleep(4)

        self.steer_arm_fixed(x=self.carry_pos[0], y=self.carry_pos[1])
        time.sleep(4)

    def return_to_carry_position(self):
        self.steer_arm_fixed(z=self.carry_pos[2])
        time.sleep(4)

        self.steer_arm_fixed(x=self.carry_pos[0], y=self.carry_pos[1])
        time.sleep(4)

    def put_down_package(self, station):
        left = station.is_left()
        log.info("Putting down package on %s side." %["right", "left"][left])
        self.set_speed(0, 0)

        if left:
            x = abs(self.arm_return_pos[0]) * -1
        else:
            x = abs(self.arm_return_pos[0])

        self.arm_return_pos[0] = x

        self.steer_arm_fixed(x=self.arm_return_pos[0], y=self.arm_return_pos[1])
        time.sleep(4)

        self.steer_arm_fixed(z=self.arm_return_pos[2])
        time.sleep(4)

        self.steer_arm_fixed(g=self.carry_pos[5])
        time.sleep(4)

        self.return_to_default_position()

        self.has_package = self.shared["hasPackage"] = False

    def is_on_stop(self):
        if len(self.station_queue) < 3:
            return False

        first = self.station_queue[0]
        second = self.station_queue[1]
        third = self.station_queue[2]

        if (first.is_left() == second.is_left() == third.is_left() and
            first.is_empty() and second.is_empty() and third.is_empty()):
            log.info("Found stop station.")
            first.empty = not self.has_package
            second.empty = not self.has_package
            third.empty = not self.has_package
            return True

    def flush_station_queue(self):
        if len(self.station_queue) == 1:
            log.info("Timeout since front station expired, trying to rescue stuff!")
            self.handle_center_station()
        else:
            log.info("Flushing station queue.")
            self.station_queue = []

    def refresh_flush_timer(self):
        self.flush_timer = time.time()

    def should_flush(self):
        timeout = 2
        if time.time() - self.flush_timer > timeout:
            return True
        else:
            return False

    def flush_command_queue(self):
        while not self.cmd_queue.empty():
            self.cmd_queue.get()

    def set_speed(self, left, right):
        if left != self.current_speed[0] or right != self.current_speed[1]:
            log.debug("set_speed: left=%d right=%d" %(left, right))

            self.current_speed[0] = self.shared["motorSpeed"][0] = left
            self.current_speed[1] = self.shared["motorSpeed"][1] = right

            self.drive.setMotorLeft(left)
            self.drive.setMotorRight(right)
            self.drive.sendAllMotor()

    def steer_arm(self, x, y, z, p, w, g):
        self.shared["armPosition"][0] += x
        self.shared["armPosition"][1] += y
        self.shared["armPosition"][2] += z
        self.shared["armPosition"][3] += p
        self.shared["armPosition"][4] += w
        self.shared["armPosition"][5] += g

        log.info("steer_arm: x=%d y=%d z=%d p=%d w=%d g=%d"
                 %(self.shared["armPosition"][0],
                   self.shared["armPosition"][1],
                   self.shared["armPosition"][2],
                   self.shared["armPosition"][3],
                   self.shared["armPosition"][4],
                   self.shared["armPosition"][5]))


        self.arm.setAll(self.shared["armPosition"])
        servo_values = self.arm.getServoValues()

        if self.arm.is_out_of_bounds():
            log.warning("Arm is out of bounds! Resetting to last good coordinates.")
            self.shared["armPosition"][0] -= x
            self.shared["armPosition"][1] -= y
            self.shared["armPosition"][2] -= z
            self.shared["armPosition"][3] -= p
            self.shared["armPosition"][4] -= w
            self.shared["armPosition"][5] -= g
        else:
            for i in range(6):
                self.drive.setArmAxis(i+1, servo_values[i])
                time.sleep(0.001)
                self.drive.sendAllAxis()
                time.sleep(0.001)

def save_cal_to_file(shared_stuff):
    f = open("calibrat.txt", "w")
    f.truncate()

    for i in ["lineCalMin", "lineCalMax", "middleCalMin", "middleCalMax"]:
        f.write(" ".join(str(e) for e in shared_stuff[i]) + "\n")

    f.close()

def load_cal_from_file(shared_stuff):
    f = open("calibrat.txt", "r")

    keys = ["lineCalMin", "lineCalMax", "middleCalMin", "middleCalMax"]
    i = 0

    for line in f:
        shared_stuff[keys[i]] = [int(e) for e in line.split()]
        i += 1

    f.close()

if __name__ == "__main__":
    line_cal_max = [213, 206, 232, 180, 232, 174, 237, 183, 199, 177, 178]
    line_cal_min = [75, 97, 126, 61, 147, 39, 154, 57, 80, 63, 50]

    middle_cal_max = [250, 250]
    middle_cal_min = [150, 150]

    shared_stuff = {"lineSensor" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "lineCalMax" : line_cal_max,
                    "lineCalMin" : line_cal_min,
                    "middleCalMax" : middle_cal_max,
                    "middleCalMin" : middle_cal_min,
                    "middleSensor" : [0, 0],
                    "distance" :  [0, 0],
                    "armPosition" : [0, 100, 130, 0, 150, 140],
                    "errorCodes" : ["Yngve Programmed Me Right"],
                    "motorSpeed" : [70, 70],
                    "latestCalibration" : "0000-00-00-15:00",
                    "autoMotor" : False,
                    "autoArm" : False,
                    "regulator" : [0, 0],
                    "error" : 0,
                    "state" : None,
                    "hasPackage" :False}

    load_cal_from_file(shared_stuff)

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

    log.basicConfig(level=log.INFO)
    gloria = Gloria(shared_stuff, cmd_queue, sensor_thread)

    try:
        gloria.run()
    except:
        gloria.set_speed(0, 0)
        sys.exit(1)
