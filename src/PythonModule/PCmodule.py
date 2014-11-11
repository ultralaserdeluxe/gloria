#PC

import socket, select, string, sys
 
#main function
if __name__ == "__main__":
     
    if len(sys.argv) < 3:
        print ('Usage : python telnet.py hostname port')
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try:
        s.connect((host, port))
    except:
        print("Unable to connect")
        sys.exit()
     
    print("Connected to remote host")
     
    while 1:
        #print("Looping")
        socket_list = [s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096).decode("ISO-8859-1")
                if not str(data):
                    print ("Connection closed")
                    sys.exit()
                else:
                    #print data
                    print(str(data))
             
            #user entered a message, was indented before, resulting in no talk
            #msg = "exit"
            msg = sys.stdin.readline()
            s.send(msg.encode("UTF-8"))

