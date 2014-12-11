import time
import Queue
import logging as log

import pcThread
import regulator
import driveUnit
import sensorThread

MANUAL = "MANUAL"
SEARCH_PICK_UP = "SEARCH_PICK_UP"
AFTER_PICK_UP = "AFTER_PICK_UP"

class Gloria:
    def __init__(self, shared_stuff, cmd_queue):
        self.shared_stuff = shared_stuff
        self.cmd_queue = cmd_queue
        self.state = MANUAL
        self.has_package = False

    def get_command(self):
        if not self.cmd_queue.empty():
            cmd = self.cmd_queue.get()
            log.debug("Got command: %s" %str(cmd))
            return cmd
        return ["NO_CMD"]

    def change_state(self, new_state):
        log.info("Changing state from %s to %s." %(self.state, new_state))        
        self.state = new_state

    def pick_up_station_found(self):
        return False

    def run(self):
        while True:
            time.sleep(0.1)
            _cmd = self.get_command()
            cmd = _cmd[0]
            args = _cmd[1:]

            # TODO: Handle calibrate commands here
            if cmd == "calibrate":
                pass

            # State transitions
            if cmd == "autoMotor" and args[0] == False:
                self.change_state(MANUAL)
            elif self.state != SEARCH_PICK_UP and not self.has_package or (cmd == "autoMotor" and args[0] == True):
                self.change_state(SEARCH_PICK_UP)
            elif self.pick_up_station_found():
                self.change_state(MANUAL)
            elif cmd == "hasPackage":
                self.state = AFTER_PICK_UP
            
            # State execution
            if self.state == MANUAL:
                self.manual(cmd, args)
            elif self.state == SEARCH_PICK_UP:
                self.search_pick_up()

    def manual(self, cmd, args):
        if cmd == "motorSpeed":
            # Set motor speed
            pass
        elif cmd == "armPosition":
            # Set arm position
            pass

    def search_pick_up(self):
        # Regulate
        pass

    def after_pick_up(self):
        # Go forward a little bit and lift arm
        pass

if __name__ == "__main__":
    ## TODO: MOVE TO SENSOR THREAD
    # calibrate_data = [[74, 198], [127, 210], [150, 220], [50, 184],
    #                  [140, 226], [65, 180], [170, 230], [47, 160],
    #                  [103, 204], [56, 165], [48, 178]]

    shared_stuff = {"lineSensor" : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "distance" :  [0, 0],
                    "armPosition" : [0, 0, 255, 4, 5, 5],
                    "errorCodes" : ["YngveProgrammedMeWrong"],
                    "motorSpeed" : [70, 70],
                    "latestCalibration" : "0000-00-00-15:00",
                    "autoMotor" : True,
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
