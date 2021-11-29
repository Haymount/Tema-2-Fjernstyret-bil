import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
  
RpiGPIO = [22,27,15,18,17,14]
  
# Set all pins as output
for pinref in RpiGPIO:
  print("Setup pins")
  GPIO.setup(pinref,GPIO.OUT)
  

StepCounter = 0
StepDir = 1
WaitTime = 0.1
  

StepCount2 = 9
Seq2 = []
Seq2 = list(range(0,StepCount2))
Seq2[0] =[0,0,0,0,0,0]
Seq2[1] =[1,0,0,0,0,0]
Seq2[2] =[1,1,0,0,0,0]
Seq2[3] =[1,1,1,0,0,0]
Seq2[4] =[0,1,1,1,0,0]
Seq2[5] =[0,0,1,1,1,0]
Seq2[6] =[0,0,0,0,1,1]
Seq2[7] =[0,0,0,0,0,1]
Seq2[8] =[0,0,0,0,0,0]
#Seq2[9] =[0,0,0,0,0,1]
#Seq2[10] =[0,0,0,0,1,1]


  

Seq = Seq2
StepCount = StepCount2
  

while True:
  print("-- Step : "+ str(StepCounter) +" --")
  for pinref in range(0, 6):
    xpin=RpiGPIO[pinref]#
    # Check if LED should be on or off
    if Seq[StepCounter][pinref]!=0:
      print(" Enable " + str(xpin))
      GPIO.output(xpin, True)
    else:
      print(" Disable " + str(xpin))
      GPIO.output(xpin, False)
  
  StepCounter += StepDir
  
  if (StepCounter==StepCount) or (StepCounter<0):
    StepDir = StepDir * -1
    StepCounter = StepCounter + StepDir + StepDir
  

  time.sleep(WaitTime)