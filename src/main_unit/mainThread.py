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
                "middleSensor" : [0, 0],
                "distance" :  [0, 0],
                "armPosition" : [0, 0, 0, 0, 0, 0],
                "arm_return_pos" : [0, 0, 0, 0, 0, 0],
                "errorCodes" : ["YngveProgrammedMeWrong"],
                "motorSpeed" : [70, 70],
                "latestCalibration" : "0000-00-00-15:00",
                "autoMotor" : False,
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



stopstation_left_detected = False
stop_cnt = 0
floor_middle = False
floor_left = False

is_centered = False

#spi init for driveunit
drive = driveUnit()
robot_arm = robotArm()

command = ["assjammer"]
# commandQueue.put(["start"])
# commandQueue.put(["autoMotor", [True]])

def check_pick_up_right():
    if is_station_right():
        #print "pick up station to the right found! error", abs(shared_stuff["error"]), is_on_straight()
        if has_package_right():
            #print "pick up station has package\n"
            if has_package == False:
                #print "has no current package, pick up\n"
                return True
    return False

def check_pick_up_left():
    if is_station_left():
        #print "pick up station to the left found! error", abs(shared_stuff["error"]), is_on_straight()
        if has_package_left():
            #print "pick up station has package\n"
            if has_package == False:
                #print "has no current package, pick up\n"
                return True
    return False           

def check_put_down_right():
    if is_station_right():
        #print "put down station to the right found! error", abs(shared_stuff["error"]), is_on_straight()
        if not has_package_right():
            #print "put down station has no package\n"
            if has_package == True:
                #print "has current package, put down\n"
                return True
    return False

def check_put_down_left():
    if is_station_left():
        #print "put down station to the left found! error", abs(shared_stuff["error"]), is_on_straight()
        if not has_package_left():
            #print "put down station has no package\n"
            if has_package == True:
                #print "has current package, put down\n"
                return True
    return False            


def is_on_straight():
    return abs(shared_stuff["error"]) < 3


def stopstation_left():
    global floor_left
    global floor_middle
    global stop_cnt

    # front sensor
    if is_station_left() and floor_left:
        stop_cnt += 1
        floor_left = False
        #time.sleep(0.15)
    elif (not is_station_left()):
        floor_left = True
    
    # middle sensor
    if station_centered() and floor_middle:
        stop_cnt-= 1
        floor_middle = False
        #time.sleep(0.15)
    elif (not station_centered()):
        floor_middle = True
    if stop_cnt > 2:
        return True
    return False

#checks if station is under robot
def station_centered():
    left_max = 250
    left_min = 150
    left_value = shared_stuff["middleSensor"][0]
    left_norm_value = float(left_value - left_min) / (left_max - left_min)

    right_max = 250
    right_min = 150
    right_value = shared_stuff["middleSensor"][1]
    right_norm_value = float(right_value - right_min) / (right_max -right_min)

    #if right_norm_value > 0.8:
    #    tape_right = True
    #else:
    #    tape_right = False
    if left_norm_value > 0.8:
        tape_left = True
    else:
        tape_left = False


    #if tape_left == True:
        #print "TAPE CENTERED DETECTED"
#    print "tape_right", tape_right, "floor_left", floor_left, "tape_value", norm_value, "floor_value", norm_value2

    return tape_left # or tape_right 



#check the sensor furthermost to the right
def is_station_right():    

    tape_max = calibrateData[8][1]
    tape_min = calibrateData[8][0]
    value = shared_stuff["lineSensor"][8]
    norm_value = float(value - tape_min) / (tape_max - tape_min)

    floor_max = calibrateData[2][1]
    floor_min = calibrateData[2][0]
    value2 = shared_stuff["lineSensor"][2]
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


#check the sensor furthermost to the left
def is_station_left():

    left = []
    right = []

    for i in range(0,3):
        tape_min = calibrateData[i][0]
        tape_max = calibrateData[i][1]
        value = shared_stuff["lineSensor"][i]
        norm_value = float(value - tape_min) / (tape_max - tape_min)
        
        floor_min = calibrateData[10][0]
        floor_max = calibrateData[10][1]
        value2 = shared_stuff["lineSensor"][10]
        norm_value2 = float(value2 - floor_min) / (floor_max - floor_min)

        if norm_value > 0.8:
            left.append(True)
            #tape_left = True
        else:
            left.append(False)
            #tape_left = False
        if norm_value2 < 0.45:
            #right.append(True)
            floor_right = True
        else:
            #right.append(False)
            floor_right= False

    #print "tape_left", tape_left, "floor_right", floor_right, "tape_value", norm_value, "floor_value", norm_value2
        
    #return tape_left and floor_right and is_on_straight()
    return left[0] and left[1] and left[2] and floor_right


#check for package on right side
def has_package_right():
    distance = distance_right(shared_stuff["distance"][0])
    #print "distanceright : ",distance
    if distance >= 6.0 and distance <= 20.0:
        return True
    return False


#check for package on left side
def has_package_left():
    distance = distance_left(shared_stuff["distance"][1])
    #print "distanceleft : ", distance
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
    global is_centered
    

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
            is_centered = False
            shared_stuff["arm_return_pos"] = shared_stuff["armPosition"][:]
            steer_arm(["fake_command", [0, 0, 100, 0, 0, 0]])
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


# Print distance sensors
# while True:
#     time.sleep(0.5)
#     #print shared_stuff["distance"]
#     has_package_left()
#     has_package_right()

# # Print middle sensor for debug
# while True:
#     time.sleep(0.5)
#     print shared_stuff["middleSensor"]

while str(commandQueue.get()[0]) != "start":
    pass
       
while True:

    #get latest PC command from queue
    get_command()
    # if True:    
    # #if automotor:
    #     if stopstation_left():
    #         if has_package:
    #             stopstation_left_detected = True
    #             put_down = False
    #         else:
    #             set_speed(0x00,0x00)
    #             automotor = False
    #     elif stop_cnt == 0:
    #         stopstation_left_detected = False

    # #print stop_cnt
    # print has_package

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
                elif (check_put_down_right() or check_put_down_left()):
                    #if not stopstation_left_detected:
                    put_down = True
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
                new_speed_left, new_speed_right = shared_stuff["regulator"]
                if station_centered():
                    is_centered = True
                if is_centered:
                    #steer arm
                    #print "Center found"
                    new_speed_left = new_speed_right = 0x00
                    set_speed(new_speed_left, new_speed_right)
                    fake_command = ["fake_command", shared_stuff["arm_return_pos"]]
                    put_down = has_package = is_centered = False
                    print "putting down package..."
                    steer_arm(fake_command)
                    time.sleep(6)
                else:
                    is_centered = False
                    set_speed(new_speed_left, new_speed_right)
        else:
            #print "Pick up True"
            #pick_up is true, user have to steer arm. pick_up = false
            new_speed_left, new_speed_right = shared_stuff["regulator"]
            if station_centered():
                is_centered = True

            if is_centered:
                #steer arm
                #print "Center found"
                new_speed_left = new_speed_right = 0x00
                if autoarm == False and command[0] == "armPosition":
                    print "Waiting for hasPackage..."
                    steer_arm(command)
            if (speed_left != new_speed_left) or (speed_right != new_speed_right):
                speed_left = new_speed_left
                speed_right = new_speed_right
                set_speed(speed_left,speed_right)
            
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
