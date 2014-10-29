from sensorThread import *
from pcThread import *
from driveUnit import *
from distance import *
from arm import robotArm
import Queue
from regulator import Regulator

################### list #######################

#calibrated data [[floor,tape],..] for every linesensor
calibrateData=[[74,198],[127,210],[150,220],[50,184],[140,226],[65,180],
                     [170,230],[47,160],[103,204],[56,165],[48,178]]


#gets fresh values from sensorthread
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

#commandos from PC
commandQueue = Queue.Queue()

################### variables #####################
#may need more...
pick_up = False
put_down = False  
automotor = False
autoarm = False
has_package = False
speed = 0x00
new_speed = 0x00
speed_left = 0x00
speed_right = 0x00
new_speed_left = 0x00
new_speed_right = 0x00
#used for syncing station, package detection
timestamp = 0
station_right = False
station_left = False
#used for syncing station, package detection
detection_time = 1 
#error marginal for linesensors
error_margin = 15

#used for detection stopstations
timestampstop_left = 0
timestampstop_right = 0
right_station_cnt = 0
left_station_cnt = 0
stop_detection_time = 2
on_floor_left = True
on_floor_right = True

#spi init for driveunit
drive = driveUnit()
robot_arm = robotArm()

command = ["assjammer"]
# commandQueue.put(["start"])
# commandQueue.put(["autoMotor", [True]])

def check_pick_up_right():
    if station_right:
        print "pick up station to the right found! error", abs(shared_stuff["error"]), is_on_straight()
        if has_package_right():
            print "pick up station has package\n"
            if has_package == False:
                print "has no current package, pick up\n"
                return True
    return False

def check_pick_up_left():
    if station_left:
        print "pick up station to the left found! error", abs(shared_stuff["error"]), is_on_straight()
        if has_package_left():
            print "pick up station has package\n"
            if has_package == False:
                print "has no current package, pick up\n"
                return True
    return False           

def check_put_down_right():
    if station_right:
        print "put down station to the right found! error", abs(shared_stuff["error"]), is_on_straight()
        if not has_package_right():
            print "put down station has no package\n"
            if has_package == True:
                print "has current package, put down\n"
                return True
    return False

def check_put_down_left():
    if station_left:
        print "put down station to the left found! error", abs(shared_stuff["error"]), is_on_straight()
        if not has_package_left():
            print "put down station has no package\n"
            if has_package == True:
                print "has current package, put down\n"
                return True
    return False            

def stopstation_left():
    global on_floor_left
    global left_station_cnt
    global timestampstop_left
    
    if (time.time() - timestampstop_left) >= stop_detection_time:
        left_station_cnt = 0
    if (is_station_left() and on_floor_left == True):
        if left_station_cnt == 0:
            timestampstop_left = time.time()
        elif left_station_cnt == 2:
            left_station_cnt = 0
            on_floor_left = False
            return True
        left_station_cnt += 1
        on_floor_left = False
        return False
    elif (not is_station_left()):
        on_floor_left = True
    return False

def stopstation_right():
    global on_floor_right
    global right_station_cnt
    global timestampstop_right

    if (time.time() - timestampstop_right) >= stop_detection_time:        
        right_station_cnt = 0
    if (is_station_right() and on_floor_right == True):
        if right_station_cnt == 0:
            timestampstop_right = time.time()
        elif right_station_cnt == 2:
            right_station_cnt = 0
            on_floor_right = False
            return True
        right_station_cnt += 1
        on_floor_right = False
        return False
    elif (not is_station_right()):
        on_floor_right = True
    return False

def is_on_straight():
    return abs(shared_stuff["error"]) < 3

#check the 3 sensors furthermost to the right
def is_station_right():
    tape_max = calibrateData[10][1]
    tape_min = calibrateData[10][0]
    value = shared_stuff["lineSensor"][10]
    norm_value = float(value - tape_min) / (tape_max - tape_min)

    floor_max = calibrateData[0][1]
    floor_min = calibrateData[0][0]
    value2 = shared_stuff["lineSensor"][0]
    norm_value2 = float(value2 - floor_min) / (floor_max - floor_min)

    if norm_value > 0.8:
        tape_right = True
    else:
        tape_right = False
    if norm_value2 < 0.45:
        floor_left = True
    else:
        floor_left = False
 
#    print "tape_right", tape_right, "floor_left", floor_left, "tape_value", norm_value, "floor_value", norm_value2

    return tape_right and floor_left and is_on_straight()


#check the 3 sensors furthermost to the left
def is_station_left():
    tape_min = calibrateData[0][0]
    tape_max = calibrateData[0][1]
    value = shared_stuff["lineSensor"][0]
    norm_value = float(value - tape_min) / (tape_max - tape_min)

    floor_min = calibrateData[10][0]
    floor_max = calibrateData[10][1]
    value2 = shared_stuff["lineSensor"][10]
    norm_value2 = float(value2 - floor_min) / (floor_max - floor_min)

    if norm_value > 0.8:
        tape_left = True
    else:
        tape_left = False
    if norm_value2 < 0.45:
        floor_right = True
    else:
        floor_right= False

#    print "tape_left", tape_left, "floor_right", floor_right, "tape_value", norm_value, "floor_value", norm_value2

    return tape_left and floor_right and is_on_straight()

#check for package on right side
def has_package_right():
    distance = distance_right(shared_stuff["distance"][0])
    if distance >= 6.0 and distance <= 20.0:
        return True
    return False


#check for package on left side
def has_package_left():
    distance = distance_left(shared_stuff["distance"][1])
    if distance >= 6.0 and distance <= 20.0:
        return True
    return False


def steer_arm(command):
    robot_arm.setAll(command[1])
    servo_values = robot_arm.getServoValues()
    for i in range(6):
        drive.setArmAxis(i+1, servo_values[i])
        time.sleep(0.001)
        drive.sendAllAxis()
        time.sleep(0.001)


def calibrate_floor(): 
    #give floor values
    for i in range(0,11):
        calibrateData[i][0] = shared_stuff["lineSensor"][i]


def calibrate_tape():
    #give tape values
    for i in range(0,11):
        calibrateData[i][1] = shared_stuff["lineSensor"][i]


def set_speed(left,right):
    drive.setMotorLeft(left)
    drive.setMotorRight(right)
    drive.sendAllMotor()

def get_command():
    #get latest PC command from queue
    global command
    global automotor
    global autoarm
    global speed
    global new_speed
    global pick_up
    global has_package
    if not commandQueue.empty():
        command = commandQueue.get()
        #print str(command)
        if command[0] == "calibrate_floor":
            calibrate_floor()
        elif command[0] == "calibrate_tape":
            calibrate_tape()
        elif str(command[0]) == "autoMotor":
            if command[1] == True:
                automotor = True
                speed_right=speed_left = 0x00
                new_speed_right=speed_right = 0x00
            else:
                automotor = False
                set_speed(0x00,0x00)
        elif command[0] == "autoArm":
            if command[1] == True:
                autoarm = True
            else:
                autoarm = False
        elif str(command[0]) == "hasPackage" and pick_up == True:
            has_package = True
            pick_up = False
        else:
            pass


#test
#commandQueue.put(["start"])
#commandQueue.put(["autoMotor",[True]])
#commandQueue.put(["autoArm",[False]])

sensorthread = sensorThread(shared_stuff)
sensorthread.daemon=True
sensorthread.start()

pcthread = pcThread(commandQueue, shared_stuff)
pcthread.daemon=True
pcthread.start()

regulator = Regulator(shared_stuff)
regulator.daemon=True
regulator.start()

while str(commandQueue.get()[0]) != "start":
    pass

while True:

    #get latest PC command from queue
    get_command()
    #if we pass a station we have *detection time* to find a package
    if timestamp == 0:
        if is_station_right():
            station_right = True
            timestamp = time.time()
        elif is_station_left():
            station_left = True
            timestamp = time.time()
        else:
            pass
    elif (time.time() - timestamp) >= detection_time:
        station_right = False
        station_left = False
        timestamp = 0
    else:
        pass
    
    
    #check if robot is on stopstation, goes into manualmode
    if stopstation_left():
        set_speed(0x00,0x00)
        automotor = False
        
    if stopstation_right():
        set_speed(0x00,0x00)
        automotor = False

    #the steerlogic.
    if automotor == True:
        if pick_up == False:
            #no need to steer arm, continue
            #check if we want to steer it anyway
            if autoarm == False:
                #steer arm
                if command[0] == "armPosition":
                    steer_arm(command)
            if put_down == False:
                if check_pick_up_right() or check_pick_up_left():
                    pick_up = True
                    new_speed_left = new_speed_right = 0x00
                elif check_put_down_right() or check_put_down_left():
                    print "jajamen"
                    put_down = True
                    new_speed_left = new_speed_right  = 0x00
                else:
                    pick_up = False
                    put_down = False                    
                    new_speed_left, new_speed_right = shared_stuff["regulator"]
                if (speed_left != new_speed_left) or (speed_right != new_speed_right):
                    speed_left = new_speed_left
                    speed_right = new_speed_right
                    set_speed(speed_left,speed_right)
            else:
                #put down package... must set put_down to false again
                print "putting down package..."                        
        else:
            print "Waiting for hasPackage..."
            #pick_up is true, user have to steer arm. pick_up = false
            if autoarm == False:
                #steer arm
                if command[0] == "armPosition":
                    steer_arm(command)
    else:
        #manuell
        if command[0] == "motorSpeed":
            new_speed_left = command[1][0]
            new_speed_right = command[1][1]
            if (speed_left != new_speed_left) or (speed_right != new_speed_right):
                speed_left = new_speed_left
                speed_right = new_speed_right
                set_speed(speed_left,speed_right)
        elif command[0] == "armPosition":
            steer_arm(command)
        else:
            pass
               
    #print "pick_up? = " + str(pick_up) + "\nput_down? = " + str(put_down)
    time.sleep(0.01)
