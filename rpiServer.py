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
g.setup(16, g.OUT)
g.setup(20, g.OUT)
g.setup(12, g.OUT)

p = g.PWM(16, 50)

p.start(18)

g.output(20, 1)

g.output(12, 1)

def motorctrl(retning):
    match retning:
        case '18':
            return 1
        case '13':
            return 2
        case '14':        
            return 0
        case '15':



while True:
    forbindelse, addresse = skt.accept()
    print("Værten med " + str(addresse[0]) + " har etableret forbindelse.")
    
    while True:
        
        data = forbindelse.recv(64)
        decdata = data.decode("UTF-8")
        
        if data:
            print("Data: ", decdata)


        else:
            print("Ikke mere data.\n")
            forbindelse.close()
            break
    
    motorctrl(decdata)


