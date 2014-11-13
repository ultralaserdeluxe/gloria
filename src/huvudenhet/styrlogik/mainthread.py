
 #[start,automotor,autoarm,harpaket]
commando = [True,True,False,False]

def main():

    pick_up = False
    put_down = False   
    
    #start?
    if commando[0] == True:
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
                    print "driving forward..."
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


main()
