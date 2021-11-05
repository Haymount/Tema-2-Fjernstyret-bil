# -*- coding: utf-8 -*-

import socket
from typing import Match
import RPi.GPIO as g


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

en1 = g.PWM(12, 75)
en2 = g.PWM(13, 75)
en1.start(0)
en2.start(0)

g.output(12, 1) #en1
g.output(16, 1) #m1

g.output(13, 1) #en2
g.output(26, 1) #m2

def motorctrl(b,c):
    en1.ChangeDutyCycle(b)
    en2.ChangeDutyCycle(c)





while True:

    forbindelse, addresse = skt.accept()
    print("Værten med " + str(addresse[0]) + " har etableret forbindelse.")
    
    while True:
        
        hdata = 0
        vdata = 0
        data = forbindelse.recv(64)
        decdata = data.decode("UTF-8")
        
        if (decdata[0] == "h"):
            #print("l57")
            hdata = decdata.replace("h","")
            print("hdata: " + hdata)
            hdata = int(hdata)
        
        elif (decdata[0] == "v"):
            #print("l63")
            vdata = decdata.replace("v","")
            print(vdata)
            vdata = int(vdata)



        if data:
            print("Data: ", decdata)
            motorctrl(hdata, vdata)
            



        else:
            print("Ikke mere data.\n")
            forbindelse.close()
            break
    
        


