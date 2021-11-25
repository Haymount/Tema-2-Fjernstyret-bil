# -*- coding: utf-8 -*-

import socket
import RPi.GPIO as g
from gpiozero import MCP3008
import threading
import time


print("Kører serveren\n")

host = "192.168.1.249" # Dette er IP-adressen for Raspberry Pi
port = 4200 # Husk at portnumre på 1024 og lavere er priviligerede

skt = socket.socket() # Man kan give argumenter til denne (f.eks. om det skal være TCP eller UDP)
skt.bind((host, port))
skt.listen(1) # Lytter til indkomne forbindelser, en ad gangen

g.setmode(g.BCM)
g.setup(16, g.OUT) #m1 
g.setup(20, g.OUT) #m2
g.setup(12, g.OUT) #en1
g.setup(26, g.OUT) #m3
g.setup(21, g.OUT) #m4
g.setup(13, g.OUT) #en2
g.setup(7, g.IN)

en1 = g.PWM(12, 100)
en2 = g.PWM(13, 100)
en1.start(0)
en2.start(0)


def motorpol(a): #Retningsstyring
    if a == 1: #Fremad
        g.output(20, 0) #m2
        g.output(16, 1) #m1
        g.output(21, 0) #m4
        g.output(26, 1) #m3
    if a == 0: #Tilbage
        g.output(20, 1) #m2
        g.output(16, 0) #m1
        g.output(21, 1) #m4
        g.output(26, 0) #m3

def motorctrl(a,b,c):
    motorpol(a)

    en1.ChangeDutyCycle(b)
    en2.ChangeDutyCycle(c)


adc = MCP3008(channel=7, select_pin=8)
def batvoltage():

    voltage = round((adc.value*3.3)*(74/27), 2) #Her udregnes spændingen om fra den værdi adc værdi vi får. gpiozero laver adc værdien om til et tal mellem 0 og 1.
    print("voltage: " + str(voltage))

    strvoltage = str(voltage)
    return strvoltage

def batklient():
    msgFromClient = batvoltage()
    bytesToSend = msgFromClient.encode("UTF-8")

    bufferSize = 1024

    # Server IP address and Port number, change the IP address and port so it is acording to the servers

    serverAddressPort = ("192.168.1.100", 4400)

    # Connect2Server forms the thread - for each connection made to the server
    def Connect2Server():
        # Create a socket instance - A datagram socket
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Send message to server using created UDP socket
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)
        # Receive message from the server
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = "Message from Rover {}".format(msgFromServer[0])
        print(msg)

    # Example show that server can handle many connections  (ThreadCount is the number of connections)
    # The following should be rewritten to the need of the application
    print("Client - Main thread started")
    ThreadList = []
    ThreadCount = 20

    for index in range(ThreadCount):
        ThreadInstance = threading.Thread(target=Connect2Server())
        ThreadList.append(ThreadInstance)
        ThreadInstance.start()

    # Here we just wait to all connection threads are complete
    for index in range(ThreadCount):
        ThreadList[index].join()

def knightriderlys():
        time.sleep(0.2)
        print("lys kører")


#Loop starter her:
while True:
    
    forbindelse, addresse = skt.accept()
    skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Værten med " + str(addresse[0]) + " har etableret forbindelse.")

    rdata = 0
    hdata = 0
    vdata = 0

    
    #x = threading.Thread(target=knightriderlys())
    #x.start()
    while True:
        
            
        data = forbindelse.recv(64)
        decdata = data.decode("UTF-8")
        arrdata = decdata.split(",")

        try:
            rdata = arrdata[0] #Retnings styring
            vdata = arrdata[2] #Venstre motor
            hdata = arrdata[1] #Højre motor
        except IndexError:
            forbindelse.close()
    

        if data:
            print("Data: ", decdata)
            motorctrl(int(rdata), int(vdata), int(hdata))
            #batklient()
        else:
            print("Klienten har lukket forbindelsen.\n")
            forbindelse.close()
            break
        
            




    
        


