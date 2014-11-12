#PC

import socket, select, string, sys, PCGUI

gui = str(input("Use GUI? (y/n) "))

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
    if gui == 'y': 
        while 1:
            PCGUI.main() #can run parallell ?
            socket_list = [s]
             
            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
             
            for sock in read_sockets:
                #incoming message from remote server
                if sock == s:
                    unparsed_data = sock.recv(4096).decode("ISO-8859-1")
                    data = str(unparsed_data)
                    if not data:
                        print ("Connection closed")
                        sys.exit()
                    else:
                        print(data)
                #Need to know what happens in the GUI
                #COULD code in the entire GUI here, but is a bad idea
                #Would be best if the GUI could send data across files. BAZINGA
                file = open("command.txt", "r")
                msg = str(file.read())
                while not msg: #wait for GUI to submit something to file
                    msg = str(file.read())
                file.close()
                s.send(msg.encode("UTF-8"))
    else:
        #Shell version
        while 1:
            socket_list = [s]
             
            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
             
            for sock in read_sockets:
                #incoming message from remote server
                if sock == s:
                    unparsed_data = sock.recv(4096).decode("ISO-8859-1")
                    data = str(unparsed_data)
                    if not data:
                        print ("Connection closed")
                        sys.exit()
                    else:
                        print(data)
                 
                #user entered a message, was indented before, resulting in no talk
                #msg = "exit"
                msg = sys.stdin.readline()
                s.send(msg.encode("UTF-8"))

