import RPi.GPIO as g
import time
from rrb2 import *
import sys
import termios

def getch():
    fd = sys.stdin.fileno()
    old_settings = terminos.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
pwmPin = 18
dc = 10
g.setmode(g.BCM)
g.setup(pwmPin, g.OUT)
pwm = g.PWM(pwmPin, 320)
rr = RRB2()
pwm.start(dc)
rr.set_led1(1)
var = 'n'
speed1 = 0
speed2 = 0
direction1 = 1
direction2 = 1

while var != 'q':
    var = getch()
    if var == 'a':
        speed1 = 0.5
        direction2 = 1
    if var == 'w':
        speed2= 0.5
        direction2 = 0
    if var == 's':
        speed2 = 0.1
        direction = 0
    if var == 'a':
        speed1 = 1
        direction1 = 1
    if var == 'd':
        speed1 = 1
        direction1 = 1
    rr.set_motors(speed1, direction1, speed2, direction2)
    time.sleep(0.1)

pwm.stop()
g.cleanup()
    