from sensorThread import *
from pcThread import *
from driveUnit import *
from distance import *
import Queue
import copy

################### list #######################

#calibrated data [[floor,tape],..] for every linesensor
calibrateData=[[74,198],[127,210],[150,220],[50,184],[140,226],[65,180],
                     [170,230],[47,160],[103,204],[56,165],[48,178]]


#gets fresh values from sensorthread
sensorList = [["lineSensor",[0,0,0,0,0,0,0,0,0,0,0]],
              ["distance",[0,0]],
              ["autoMotor",[True]],
              ["autoArm",[False]],
              ["motorSpeed",[0,0]]]

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
timestampstop = 0
right_station_cnt = 0
stop_detection_time = 1

#spi init for driveunit
drive = driveUnit()

command = ["assjammer"]

def check_pick_up_right():
    if station_right:
        print "station to the right found\n"
        if has_package_right():
            print "station has package\n"
            if has_package == False:
                #print "has no current package, pick up\n"
                return True
    return False

def check_pick_up_left():
    if station_left:
        print "station to the left found\n"
        if has_package_left():
            print "station has package\n"
            if has_package == False:
                #print "has no current package, pick up\n"
                return True
    return False           

def check_put_down_right():
    if station_right:
        #print "station to the right found\n"
        if not has_package_right():
            #print "station has no package\n"
            if has_package == True:
                #print "has current package, put down\n"
                return True
    return False

def check_put_down_left():
    if station_left:
        #print "station to the left found\n"
        if not has_package_left():
            #print "station has no package\n"
            if has_package == True:
                #print "has current package, put down\n"
                return True
    return False            


#if we have 3 stations without packages in a row??
def on_stopstation_right():
    global timestampstop
    global right_station_cnt
    if timestampstop == 0:
        timestampstop = time.time()
    elif (time.time() - timestampstop) <= stop_detection_time:
        if is_station_right() and right_station_cnt == 2:
            right_station_cnt = 0
            timestampstop = 0
            return True
        elif is_station_right and right_station_cnt != 2:
            right_station_cnt += 1
        else:
            pass
    else:
        timestampstop = 0
        right_station_cnt = 0
    return False

#check the 3 sensors furthermost to the right
def is_station_right():
    tape_max = calibrateData[10][1]
    tape_min = calibrateData[10][0]
    value = sensorList[0][1][10]
    norm_value = float(value - tape_min) / (tape_max - tape_min)

    floor_max = calibrateData[0][1]
    floor_min = calibrateData[0][0]
    value2 = sensorList[0][1][0]
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

    return tape_right and floor_left


#check the 3 sensors furthermost to the left
def is_station_left():
    tape_min = calibrateData[0][0]
    tape_max = calibrateData[0][1]
    value = sensorList[0][1][0]
    norm_value = float(value - tape_min) / (tape_max - tape_min)

    floor_min = calibrateData[10][0]
    floor_max = calibrateData[10][1]
    value2 = sensorList[0][1][10]
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

    return tape_left and floor_right


#check for package on right side
def has_package_right():
    distance = distance_right(sensorList[1][1][0])
    if distance >= 6.0 and distance <= 20.0:
        return True
    return False


#check for package on left side
def has_package_left():
    distance = distance_left(sensorList[1][1][1])
    if distance >= 6.0 and distance <= 20.0:
        return True
    return False


def drive_forward():
    print "keep on truckin..."


def steer_arm(command):
    axis_id = 1
    for data in command[1]:
        drive.setArmAxis(axis_id,data)
        axis_id+=1
    drive.sendAllAxis()


def calibrate_floor(): 
    #give floor values
    for i in range(0,11):
        calibrateData[i][0] = sensorList[0][1][i]


def calibrate_tape():
    #give tape values
    for i in range(0,11):
        calibrateData[i][1] = sensorList[0][1][i]


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
    if not commandQueue.empty():
        command = commandQueue.get()
        #print command
        if command[0] == "calibrate_floor":
            calibrate_floor()
        elif command[0] == "calibrate_tape":
            calibrate_tape()
        elif command[0] == "autoMotor":
            if command[1][0] == True:
                automotor = True
                speed = 0x00
                new_speed = 0x00
            else:
                automotor = False
                set_speed(0x00,0x00)
        elif command[0] == "autoArm":
            if command[1][0] == True:
                autoarm = True
            else:
                autoarm = False
        else:
            pass


#test
#ommandQueue.put(["start"])
#commandQueue.put(["autoMotor",[True]])
#ommandQueue.put(["autoArm",[False]])

sensorthread = sensorThread(sensorList)
sensorthread.daemon=True
sensorthread.start()

pcthread = pcThread(commandQueue, sensorList)
pcthread.daemon=True
pcthread.start()

#while commandQueue.get()[0] != "start":
 #   pass

while True:

    #get latest PC command from queue
    get_command()
    #print command
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
    #if on_stopstation_right():
        #print "stop station"
        #drive.setMotorLeft(0x00)
        #drive.setMotorRight(0x00)
        #drive.sendAllMotor()
        #automotor = False
    
    #the steerlogic.
    if automotor == True:
        #print "autonom motor\n"
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
                    new_speed = 0x00
                elif check_put_down_right() or check_put_down_left():
                    put_down = True
                    new_speed = 0x00
                else:
                    pick_up = False
                    put_down = False                    
                    new_speed = 0x40
                if speed != new_speed:
                    speed = new_speed
                    set_speed(speed,speed)
            else:
                #put down package... must set put_down to false again
                print "putting down package..."                        
        else:
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
