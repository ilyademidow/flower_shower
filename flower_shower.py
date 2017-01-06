# Reading an analogue sensor with
# a single GPIO pin

# Author : Matt Hawkins
# Distribution : Raspbian
# Python : 2.7
# GPIO   : RPi.GPIO v3.1.0a

import RPi.GPIO as GPIO, time
from gpiozero import OutputDevice

# Tell the GPIO library to use
# Broadcom GPIO references
GPIO.setmode(GPIO.BCM)
outD = OutputDevice(17)

# Define function to measure charge time
print("LOW " + str(GPIO.LOW))
print("OUT " + str(GPIO.OUT))
def RCtime (PiPin):
  measurement = 0
  # Discharge capacitor
  GPIO.setup(PiPin, GPIO.OUT)
  GPIO.output(PiPin, GPIO.LOW)
  time.sleep(0.01)

  GPIO.setup(PiPin, GPIO.IN)
  # Count loops until voltage across
  # capacitor reads high on GPIO
  for i in range(0,1000):
    if (GPIO.input(PiPin) == GPIO.LOW):
        measurement += 1

  return measurement

# Main program loop
while True:
  moisture = int(float(RCtime(9)))
  print(moisture) # Measure timing using GPIO4
  if(moisture <= 500):
      print("true (<500)")
      outD.on()
      time.sleep(3)
  else:
      print("false (<500)")
      outD.off()
