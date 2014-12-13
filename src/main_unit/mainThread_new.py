import sys
import time
import Queue
import logging as log

import pcThread
import regulator
import driveUnit
import sensorThread
import sensor_eval as se
import arm

HALTED = "HALTED"
MANUAL = "MANUAL"
LINE = "LINE"
STATION_FRONT = "STATION_FRONT"
STATION_CENTER = "STATION_CENTER"
STATION_BOTH = "STATION_BOTH"

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

    def __str__(self):
        return "(left=%s, empty=%s)" %(str(self.left), str(self.empty))

    @staticmethod
    def create(side, package):
        log.info("Station.create side=%s package=%s" %(side, package))
        station = None

        if side == se.LEFT and package == se.LEFT:
            station = Station(False, True)
        elif side == se.LEFT and package != se.LEFT:
            station = Station(True, True)
        elif side == se.RIGHT and package == se.RIGHT:
            station = Station(False, False)
        elif side == se.RIGHT and package != se.RIGHT:
            station = Station(True, False)
        else:
            log.critical("Tried to create Station with side=\"%s\" and package=\"%s\"!" %(side, package))

        log.debug("Created Station with empty=%s and left=%s." %(str(station.is_empty()), str(station.is_left())))
        return station

class Gloria:
    def __init__(self, shared_stuff, cmd_queue, sensor_thread):
        self.shared = shared_stuff
        self.cmd_queue = cmd_queue

        self.arm = arm.robotArm()
        self.drive = driveUnit.driveUnit()
        self.current_speed = [None, None]

        self.state = None
        self.stored_state = none
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

    def store_state(self, state = None):
        if state is None: state = self.state
        log.info("Restoring state from %s to %s" %(self.state, self.stored_state))
        self.stashed_state = self.state

    def restore_state(self):
        self.change_state(self.stored_state)

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
        elif cmd == "hasPackage" and self.state == MANUAL and self.stored_state != None:
            # TODO: Add return arm to default position
            self.restore_state()
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
        self.set_speed(0, 0)

    def manual(self, cmd, args):
        if cmd == "calibrateFloor":
            sensor_thread.calibrateFloor()
            pass
        elif cmd == "calibrateTape":
            sensor_thread.calibrateTape()
            pass
        elif cmd == "motorSpeed":
            self.set_speed(args[0], args[1])
        elif cmd == "armPosition":
            self.steer_arm(*args)

    def line(self):
        front_values = self.shared["lineSensor"][:]
        front_converted = se.convert_line_values(front_values)

        center_values = self.shared["middleSensor"][:]
        center_converted = se.convert_line_values(center_values)

        log.debug("front=%s center=%s" %(str(front_converted), str(center_converted)))

        if not se.all_equal(front_converted):
            front_station = se.station_front(front_converted)
            package = se.detect_package(*self.shared["distance"])

            if front_station != se.NO_STATION and self.is_on_straight():
                front_obj = Station.create(front_station, package)
                log.info("Found front station with empty=%s and left=%s." %(str(front_obj.is_empty()), str(front_obj.is_left())))
                self.station_queue.append(front_obj)
                log.info([str(e) for e in self.station_queue])
                self.change_state(STATION_FRONT)
            else:
                left, right = self.shared["regulator"]
                self.set_speed(left, right)

            center_station = se.station_center(center_converted)

            if center_station != se.NO_STATION and self.is_on_straight():
                self.handle_center_station()
        else:
            log.info("Found crossing or break in line.")
            self.go_straight()

    def handle_center_station(self, next_state=STATION_CENTER):
        if self.is_on_stop() and not self.has_package: self.change_state(HALTED)

        if len(self.station_queue) == 0:
            log.error("Found unknown center station!")
            self.change_state(next_state)
            return

        current_center = self.station_queue.pop(0)
        if self.has_package and not current_center.is_full():
            log.info("Current station (left=%s) has no package but robot does. Put down!" %current_center.is_left())
            log.info([str(e) for e in self.station_queue])
            self.put_down_packge()
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
        self.go_straight()

        front_values = self.shared["lineSensor"][:]
        front_converted = se.convert_line_values(front_values)
        front_station = se.station_front(front_converted)

        center_values = self.shared["middleSensor"][:]
        center_converted = se.convert_line_values(center_values)
        center_station = se.station_center(center_converted)

        if front_station == se.NO_STATION:
            log.info("Leaving front station.")
            self.change_state(LINE)
        elif center_station != se.NO_STATION and self.is_on_straight():
            log.info("Detected center station while on front station.")
            self.handle_center_station(next_state=STATION_BOTH)

    def station_center(self):
        front_values = self.shared["lineSensor"][:]
        front_converted = se.convert_line_values(front_values)
        front_station = se.station_front(front_converted)
        package = se.detect_package(*self.shared["distance"])

        center_values = self.shared["middleSensor"][:]
        center_converted = se.convert_line_values(center_values)
        center_station = se.station_center(center_converted)

        if center_station == se.NO_STATION:
            log.info("Leaving center station.")
            self.change_state(LINE)
        elif front_station != se.NO_STATION and self.is_on_straight():
            front_obj = Station.create(front_station, package)
            log.info("Found front station with empty=%s and left=%s." %(str(front_obj.is_empty()), str(front_obj.is_left())))
            self.station_queue.append(front_obj)
            log.info([str(e) for e in self.station_queue])
            self.change_state(STATION_BOTH)
        else:
            if not se.all_equal(front_converted):
                left, right = self.shared["regulator"]
                self.set_speed(left, right)
            else:
                self.go_straight()
                log.info("Found a crossing or break in line.")

    def station_both(self):
        self.go_straight()

        front_values = self.shared["lineSensor"][:]
        front_converted = se.convert_line_values(front_values)
        front_station = se.station_front(front_converted)

        center_values = self.shared["middleSensor"][:]
        center_converted = se.convert_line_values(center_values)
        center_station = se.station_center(center_converted)

        if front_station != se.NO_STATION:
            log.info("Leaving front station.")
            self.change_state(STATION_CENTER)
        elif center_station != se.NO_STATION:
            log.info("Leaving center station.")
            self.change_state(STATION_FRONT)

    def go_straight(self):
        self.set_speed(50, 50)

    def is_on_straight(self):
        avg = sum(map(abs, self.shared["pastErrors"])) / len(self.shared["pastErrors"])

        return avg < 3
        
    def put_down_package(self, station):
        side = ["right", "left"][station.is_left()]
        log.info("Putting down package on %s side." %side)
        set_speed(0, 0)
        # TODO: Steer arm

    def is_on_stop(self):
        if len(self.station_queue) < 3:
            return False

        first = self.station_queue[0]
        second = self.station_queue[1]
        third = self.station_queue[2]

        if (first.is_left() == second.is_left() == third.is_left() and
            first.is_empty() and second.is_empty() and third.is_empty()):
            log.info("Found stop station.")
            return True

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

        self.arm.setAll([x, y, z, p, w, g])
        servo_values = self.arm.getServoValues()

        for i in range(6):
            self.drive.setArmAxis(i+1, servo_values[i])
            time.sleep(0.001)
            self.drive.sendAllAxis()
            time.sleep(0.001)

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
                    "armPosition" : [0, 0, 255, 4, 5, 5],
                    "errorCodes" : ["YngveProgrammedMeWrong"],
                    "motorSpeed" : [70, 70],
                    "latestCalibration" : "0000-00-00-15:00",
                    "autoMotor" : False,
                    "autoArm" : False,
                    "regulator" : [0, 0],
                    "error" : 0,
                    "pastErrors": []}

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
    gloria.run()
