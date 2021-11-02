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

m1 = g.PWM(16, 75)
m3 = g.PWM(26, 75)
#m1.start(0)
#m3.start(0)

g.output(20, 1)
g.output(12, 1)

g.output(13, 1)
g.output(21, 1)

def motorctrl(retning):


    if retning == 18:
        m1.ChangeDutyCycle(100)
        m3.ChangeDutyCycle(100)
    
    else:
        m1.ChangeDutyCycle(0)
        m3.ChangeDutyCycle(0)




while True:
    
    
    m1.ChangeDutyCycle(0)
    m3.ChangeDutyCycle(0)
    
    forbindelse, addresse = skt.accept()
    print("Værten med " + str(addresse[0]) + " har etableret forbindelse.")
    
    while True:
        

        data = forbindelse.recv(64)
        decdata = data.decode("UTF-8")
        
        if data:
            print("Data: ", decdata)
            motorctrl(decdata)


        else:
            print("Ikke mere data.\n")
            forbindelse.close()
            break
    
        


