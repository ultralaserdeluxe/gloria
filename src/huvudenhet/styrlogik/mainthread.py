from sensorthread import *

 #[start,automotor,autoarm,harpaket,kalibrera]
commando = [True,True,False,False,True]

def main():

    #kommer nog behöva fler
    pick_up = False
    put_down = False  

    sensorthread = SensorThread(0.1)
    sensorthread.start()

    try:
        while True:
            #start?
            if commando[0] == True:
                #autonom motor och inte befinner sig på stoppstation
                if (commando[1] == True) and not on_stopstation() :
                    print "autonom motor\n"
                    if pick_up == False:
                        #behöver inte styra armen, fortsätt...
                        #kolla om vi vill styra armen ändå
                        if commando[2] == False:
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
                        if commando[2] == False:
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
            if commando[3] == False:
                print "has no current package, pick up\n"
                return True
    return False

def check_pick_up_left():
    if is_station_left():
        print "station to the left found\n"
        if has_package_left():
            print "station has package\n"
            if commando[3] == False:
                print "has no current package, pick up\n"
                return True
    return False           

def check_put_down_right():
    if is_station_right():
        print "station to the right found\n"
        if not has_package_right():
            print "station has no package\n"
            if commando[3] == True:
                print "has current package, put down\n"
                return True
    return False

def check_put_down_left():
    if is_station_left():
        print "station to the left found\n"
        if not has_package_left():
            print "station has no package\n"
            if commando[3] == True:
                print "has current package, put down\n"
                return True
    return False            

def on_stopstation():
    #om vi har haft 3 stationer utan paket på varandra? (med ett visst avstånd)
    if binary_to_int(line_sensordata) < 300 and binary_to_int(line_sensordata) > 100:
        return True
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

#tar en lista med ett binärtal och gör om det till ett heltal
def binary_to_int(seq):
    temp = ""
    for i in seq:
        temp += str(i)
    return int(temp,2)    
    

main()

