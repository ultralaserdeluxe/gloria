from sensorThread import *
#from pcThread import *
from driveUnit import *
from distance import *
import Queue

################### list #######################

#calibrated data [[floor,tape],..] for every linesensor
calibrateData=[[74,198],[127,210],[150,220],[50,184],[140,226],[65,180],
                     [170,230],[47,160],[103,204],[56,165],[48,178]]


#gets fresh values from sensorthread
sensorList = [["lineSensor",[0,0,0,0,0,0,0,0,0,0,0]],
              ["distance",[0,0]]]

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
#used for syncing station, package detection
timestamp = 0
station_right = False
station_left = False
#used for syncing station, package detection
detection_time = 3 
#error marginal for linesensors
error_margin = 5

#spi init for driveunit
drive = driveUnit()

command = []

def check_pick_up_right():
    if station_right:
        print "station to the right found\n"
        if has_package_right():
            print "station has package\n"
            if has_package == False:
                print "has no current package, pick up\n"
                return True
    return False

def check_pick_up_left():
    if station_left:
        print "station to the left found\n"
        if has_package_left():
            print "station has package\n"
            if has_package == False:
                print "has no current package, pick up\n"
                return True
    return False           

def check_put_down_right():
    if station_right:
        print "station to the right found\n"
        if not has_package_right():
            print "station has no package\n"
            if has_package == True:
                print "has current package, put down\n"
                return True
    return False

def check_put_down_left():
    if station_left:
        print "station to the left found\n"
        if not has_package_left():
            print "station has no package\n"
            if has_package == True:
                print "has current package, put down\n"
                return True
    return False            


def on_stopstation():
    #if we have 3 stations without packages in a row??
    return False

#check the 3 sensors furthermost to the right
def is_station_right():
    answer = False
    for i in range(8,11):
        value = sensorList[0][1][i]
        tape_value = calibrateData[i][1]
        if value <= (tape_value + error_margin) and value >= (tape_value - error_margin):
            answer = True
        else:
            answer = False
    return answer

#check the 3 sensors furthermost to the left
def is_station_left():
    answer = False
    for i in range(0,3):
        value = sensorList[0][1][i]
        tape_value = calibrateData[i][1]
        if value <= (tape_value + error_margin) and value >= (tape_value - error_margin):
            answer = True
        else:
            answer = False
    return answer

def has_package_right():
    distance = distance_right(sensorList[1][1][0])
    if distance >= 6.0 and distance <= 20.0:
        return True
    return False

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

                             


sensorthread = sensorThread(sensorList)
sensorthread.start()

#test
commandQueue.put(["start"])
commandQueue.put(["autoMotor",[True]])
commandQueue.put(["autoArm",[False]])


#pcthread = pcThread(sensorList,commandQueue)
#pcthread.start()

while not commandQueue.get()[0] != "start":
    pass

while True:
    #get latest PC commando from queue
    if not commandQueue.empty():
        command = commandQueue.get()
        if command[0] == "calibrate_floor":
            calibrate_floor()
        elif command[0] == "calibrate_tape":
            calibrate_tape()
        elif command[0] == "autoMotor":
            if command[1][0] == True:
                automotor = True
            else:
                automotor = False
        elif command[0] == "autoArm":
            if command[1][0] == True:
                autoarm = True
            else:
                autoarm = False
        else:
            pass

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
            
    #the steerlogic...
    if automotor == False and not on_stopstation() :
        print "autonom motor\n"
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
                    new_speed = 0x60
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
            drive.setMotorLeft(command[1][0])
            drive.setMotorRight(command[1][1])
            drive.sendAllMotor()
        elif command[0] == "armPosition":
            steer_arm(command)
        else:
            pass
               
    if speed != new_speed:
        speed = new_speed
        drive.setMotorLeft(speed)
        drive.setMotorRight(speed)
        drive.sendAllMotor()
               
    print "pick_up? = " + str(pick_up) + "\nput_down? = " + str(put_down)
    time.sleep(0.1)
