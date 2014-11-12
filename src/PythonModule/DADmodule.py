#DAD

import socket
import sys
import threading

HOST = ''   # Symbolic name meaning all available interfaces, change to IP if needed
PORT = 8888 # Arbitrary non-privileged port. Subject to change

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: 
    s.bind((HOST, PORT))
except (socket.error, msg):
    print('Bind Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

s.listen(10) #arbitrary number for amount of queue-able connections, min 0

def main(conn):
    conn.send("Hi and Welcome to Gloria, issue your command and press ENTER.\n".encode("UTF-8"))
    while True:
        #Recieving from PC, fork depending on data
        unparsed_data = conn.recv(1024).decode("ISO-8859-1") #1024 = buffer size
        data = str(unparsed_data)
        if "exit" in data:
            break
        elif "status" in data or "calibrate" in data:
            conn.send("Reply\n".encode("UTF-8")) #To be changed
        elif "start" in data:
            conn.send("Starting...\n".encode("UTF-8"))
        elif "arm" in data:
            split_data = data.split(';')
            for elem in split_data:
                conn.send((elem + "\n").encode("UTF-8"))
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
