from sensorthread import *
from pcThread import *

def main():

    #kommer nog behöva fler
    pick_up = False
    put_down = False  
    automotor = False
    autoarm = False
    has_package = False
    
    commandQueue = queue.Queue()
    sensorList = [["lineSensor",[]],
                  ["distance",[]]]
    
    sensorthread = SensorThread(sensorList)
    sensorthread.start()

    pcthread = pcThread(sensorList,commandQueue)
    pcthread.start()
    
    while commandQueue.get()[0] != "start":
        pass

    try:
        while True:
            #hämta pc kommandot från kön...
            command = commandQueue.get()
            if command[0] == "autoMotor":
                if command[1][0] == True:
                    automotor = True
                else:
                    automotor = False
            if command[0] == "autoArm":
                if command[1][0] == True:
                    autoarm = True
                else:
                    autoarm = False
            
            #utför
            if automotor == False and not on_stopstation() :
                print "autonom motor\n"
                if pick_up == False:
                    #behöver inte styra armen, fortsätt...
                    #kolla om vi vill styra armen ändå
                    if autoarm == False:
                        #styr arm
                        print "waiting for arm input...\n"
                    if put_down == False:
                        if check_pick_up_right() or check_pick_up_left():
                            pick_up = True
                        else:
                            pick_up = False
                        if check_put_down_right() or check_put_down_left():
                            put_down = True
                        else:
                            put_down = False
                            regulate()
                            drive_forward()
                    else:
                        #sätt ned paket
                        print "putting down package..."                        
                else:
                    if autoarm == False:
                        #styr arm 
                        print "waiting for arm input..."
            else:
                #manuellt läge
                print "waiting for PC input..."

                                            
            print "pick_up? = " + str(pick_up) + "\nput_down? = " + str(put_down)
            time.sleep(1)
    except KeyboardInterrupt:
        sensorthread.kill(1)
        pass



def check_pick_up_right():
    if is_station_right():
        print "station to the right found\n"
        if has_package_right():
            print "station has package\n"
            if has_package == False:
                print "has no current package, pick up\n"
                return True
    return False

def check_pick_up_left():
    if is_station_left():
        print "station to the left found\n"
        if has_package_left():
            print "station has package\n"
            if has_package == False:
                print "has no current package, pick up\n"
                return True
    return False           

def check_put_down_right():
    if is_station_right():
        print "station to the right found\n"
        if not has_package_right():
            print "station has no package\n"
            if has_package == True:
                print "has current package, put down\n"
                return True
    return False

def check_put_down_left():
    if is_station_left():
        print "station to the left found\n"
        if not has_package_left():
            print "station has no package\n"
            if has_package == True:
                print "has current package, put down\n"
                return True
    return False            

def on_stopstation():
    #om vi har haft 3 stationer utan paket på varandra? (med ett visst avstånd)
    return False

def is_station_right():
    return True

def is_station_left():
    return False

def has_package_right():
    return True

def has_package_left():
    return False

def regulate():
    print "regulating..."

def drive_forward():
    print "keep on truckin..."

def calibrate():   
    print "calibrating..."
    
