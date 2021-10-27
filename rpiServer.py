# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 16:31:55 2018

Klient/serverkode til Roverstyring på Raspberry Pi.
Denne fil indeholder serverdelen.

Version 2: Interaktiv styring fra klientens side via pygame.

@author: HTH
"""

import socket
import gpiozero as io

print("Kører serveren\n")

host = "192.168.1.249" # Dette er IP-adressen for Raspberry Pi
port = 4200 # Husk at portnumre på 1024 og lavere er priviligerede

skt = socket.socket() # Man kan give argumenter til denne (f.eks. om det skal være TCP eller UDP)
skt.bind((host, port))

skt.listen(1) # Lytter til indkomne forbindelser, en ad gangen

greenLED1 = io.LED(17)
greenLED2 = io.LED(18)
orangeLED1 = io.LED(22)
orangeLED2 = io.LED(23)
redLED = io.LED(24)

ledStatus = [0,0,0,0,0]

def toggleLED(ledID):
    if ledID == "17":
        if ledStatus[0] == 0:
            greenLED1.on()
            ledStatus[0] = 1
        else:
            greenLED1.off()
            ledStatus[0] = 0
    if ledID == "18":
        if ledStatus[1] == 0:
            greenLED2.on()
            ledStatus[1] = 1
        else:
            greenLED2.off()
            ledStatus[1] = 0
    if ledID == "22":
        if ledStatus[2] == 0:
            orangeLED1.on()
            ledStatus[2] = 1
        else:
            orangeLED1.off()
            ledStatus[2] = 0
    if ledID == "23":
        if ledStatus[3] == 0:
            orangeLED2.on()
            ledStatus[3] = 1
        else:
            orangeLED2.off()
            ledStatus[3] = 0
    if ledID == "24":
        if ledStatus[4] == 0:
            redLED.on()
            ledStatus[4] = 1
        else:
            redLED.off()
            ledStatus[4] = 0

while True:
    forbindelse, addresse = skt.accept()
    print("Værten med " + str(addresse[0]) + " har etableret forbindelse.")
    
    while True:
        
        data = forbindelse.recv(64)
        decdata = data.decode("UTF-8")
        
        if data:
            print("Data: ", decdata)
            
            toggleLED(decdata)


        else:
            print("Ikke mere data.\n")
            forbindelse.close()
            break