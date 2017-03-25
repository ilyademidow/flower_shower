# The simplest script for watering a plants by soil moisture module and water pomp
# Tuning YL-38 and connect DO to Raspberry Pi Model 3
# Output is True or False for current moisture
#
# Author : Ilya Demidov
# Distribution : Raspbian
# Python : 3
# GPIO   : RPi.GPIO v3.1.0a
import time, configparser
from gpiozero import MotionSensor, OutputDevice
from sendmail import send_mail

# Read Mode from config
config = configparser.ConfigParser()
config.read("mode.py")

debugMode = config.getboolean("Mode","debugMode")
waterValue = config.getint("Water","waterValue")
hourStart = config.getint("Start","hour")
minStart = config.getint("Start","min")

# MotionSensor class is useful for this digital output
ms = MotionSensor(17)
# Soil Moisture connect throw a NPN transistor
smDC = OutputDevice(20)
# WaterPomp
# Connect throw a NPN transistor. Really it is pinout at emitter
waterPomp = OutputDevice(21)
# Detector is it was water
waterComplete = False;

smDC.off()
waterPomp.off()

# Main program loop
while True:
  if (time.gmtime().tm_hour == hourStart and time.gmtime().tm_min == minStart):
    try:
      smDC.on()
      if ms.motion_detected:
        waterComplete = True
        if debugMode:
          print("on")
        else:
          waterPomp.on()
        time.sleep(waterValue)
      else:
        if debugMode:
          print("OFF")
        else:
          waterPomp.off()
        if (waterComplete):
          send_mail(str(time.gmtime()) + " I've finished")
          waterComplete = False
    finally:
      smDC.off()
      waterPomp.off()
      if (waterComplete):
        send_mail(str(time.gmtime()) + " Probably app shutdown unexpected")
        waterComplete = False
  else:
    if (waterComplete):
      smDC.off()
      if debugMode:
        print("OFF")
      else:
        waterPomp.off()
      send_mail(str(time.gmtime()) + " Probably app shutdown unexpected") 
      waterComplete = False
