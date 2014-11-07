#To do:
#Module for communication between DAD and PC
#Goal: To be able to send a flow of commands via shell that can be interpreted
#Main while-loop, run until clearly stated exit
#Keep sending data to socket
#Make sure buffer doesn't freak out, minimize the bogus data
#Time / Effort!

import socket
import sys
import threading

HOST = ''   # Symbolic name meaning all available interfaces, change to IP later
PORT = 8888 # Arbitrary non-privileged port. Subject to change

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: 
    s.bind((HOST, PORT))
except (socket.error, msg):
    print('Bind Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

s.listen(10) #arbitrary number for amount of queue-able connections, min 0

def main(conn):
    #may need to re-structure this...
    conn.send("Hi and Welcome to Gloria, issue your command and press ENTER.\n".encode("UTF-8"))
    while True:
        #Recieving from PC
        data = conn.recv(1024).decode("ISO-8859-1") #1024 = buffer size
        if "exit" in str(data):
            break
        elif "status" in str(data) or "calibrate" in str(data):
            conn.send("Reply\n".encode("UTF-8")) #To be changed
        conn.send("Command accepted. Please wait... ".encode("UTF-8"))
        #Gloria does something depending on command
    conn.close()

#Keep talking with PC:
while True:
    #Wait to accept a connection - blocking call
    conn, addr = s.accept()
    #Start new friend, arg1 = function to be run, arg2 = tuple to function
    threading.Thread(target=main, args=(conn,)).start()

s.close()
