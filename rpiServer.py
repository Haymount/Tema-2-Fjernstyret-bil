# -*- coding: utf-8 -*-

import socket
import RPi.GPIO as g
from gpiozero import MCP3008

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

en1 = g.PWM(12, 75)
en2 = g.PWM(13, 75)
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


#Loop starter her:
try:
    while True:
            batvoltage()
            forbindelse, addresse = skt.accept()
            print("Værten med " + str(addresse[0]) + " har etableret forbindelse.")

            rdata = 0
            hdata = 0
            vdata = 0

            while True:
                
                data = forbindelse.recv(64)
                decdata = data.decode("UTF-8")
                arrdata = decdata.split(",")

                try:
                    rdata = arrdata[0] #Retnings styring
                    vdata = arrdata[1] #Venstre motor
                    hdata = arrdata[2] #Højre motor
                except IndexError:
                    forbindelse.close()
        

                if data:
                    print("Data: ", decdata)
                    motorctrl(int(rdata), int(vdata), int(hdata))

                else:
                    print("Klienten har lukket forbindelsen.\n")
                    forbindelse.close()
                    break

except KeyboardInterrupt:
    forbindelse.close()
    g.cleanup()


    
        


