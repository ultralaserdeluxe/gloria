from sensorThread import *
from pcThread import *
from driveUnit import *
import Queue

################### list #######################

#calibrated data [[floor,tape],..] for every linesensor
linesensor_c_data = [[54,201],[122,225],[141,238],[66,177],[136,231],[76,185],
                     [171,228],[44,175],[97,195],[60,173],[43,168]]


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
#used for syncing station, package detection
timestamp = 0
detection_time = 3 
is_station_right = False
is_station_left = False
#error marginal for linesensors
error_margin = 5
                             
def main():
    
    #spi init for driveunit
    driveunit = driveUnit()

    sensorthread = sensorThread(sensorList)
    sensorthread.start()

    pcthread = pcThread(sensorList,commandQueue)
    pcthread.start()

    while commandQueue.get()[0] != "start":
        pass

    try:
        while True:
            #get latest PC commando from queue
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
                    is_station_right = True
                    timestamp = time.time()
                elif is_station_left():
                    is_station_left = True
                    timestamp = time.time()
                else:
                    pass
            elif (time.time() - timestamp) >= detection_time:
                is_station_right = False
                is_station_left = False
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
                        elif check_put_down_right() or check_put_down_left():
                            put_down = True
                        else:
                            pick_up = False
                            put_down = False
                            regulate()
                            drive_forward()
                    else:
                        #put down package... must set put_down to false again
                        print "putting down package..."                        
                else:
                    #pick_up is true, user have to steer arm. pick_up has to be set to false again
                    if autoarm == False:
                        #steer arm
                        if command[0] == "armPosition":
                            steer_arm(command)
            else:
                #manuell
                if command[0] == "motorSpeed":
                    driveunit.setMotorLeft(command[1][0])
                    driveunit.setMotorRight(command[1][1])
                    driveunit.sendAllMotor()
                elif command[0] == "armPosition":
                    steer_arm(command)
                else:
                    pass
                                            
            print "pick_up? = " + str(pick_up) + "\nput_down? = " + str(put_down)
            time.sleep(1)
    except KeyboardInterrupt:
        sensorthread.kill(1)
        pass


def check_pick_up_right():
    if is_station_right:
        print "station to the right found\n"
        if has_package_right():
            print "station has package\n"
            if has_package == False:
                print "has no current package, pick up\n"
                return True
    return False

def check_pick_up_left():
    if is_station_left:
        print "station to the left found\n"
        if has_package_left():
            print "station has package\n"
            if has_package == False:
                print "has no current package, pick up\n"
                return True
    return False           

def check_put_down_right():
    if is_station_right:
        print "station to the right found\n"
        if not has_package_right():
            print "station has no package\n"
            if has_package == True:
                print "has current package, put down\n"
                return True
    return False

def check_put_down_left():
    if is_station_left:
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
        tape_value = linesensor_c_data[i][1]
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
        tape_value = linesensor_c_data[i][1]
        if value <= (tape_value + error_margin) and value >= (tape_value - error_margin):
            answer = True
        else:
            answer = False
    return answer

def has_package_right():
    return False

def has_package_left():
    return False

def regulate():
    print "regulating..."

def drive_forward():
    print "keep on truckin..."

def steer_arm(command):
    axis_id = 1
    for data in command[1]:
        driveunit.setArmAxis(axis_id,data)
        axis_id+=1
    driveunit.sendAllAxis()

def calibrate_floor(): 
    #give floor values
    for i in range(0,11):
        linesensor_c_data[i][0] = sensorList[0][1][i]

def calibrate_tape():
    #give tape values
    for i in range(0,11):
        linesensor_c_data[i][1] = sensorList[0][1][i]

def kastman(x):
    z = (x-41)/25
    return (0.093*z**6) - (0.77*z**5) + (2.4*z**4) - (3.9*z**3) + (4.7*z**2) - (7.4*z) + 13


for x in range(0,110):
    print kastman(x)

