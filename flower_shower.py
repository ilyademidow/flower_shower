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

# Read Mode from config
config = configparser.ConfigParser()
config.read("mode.py")
debugMode = config.getboolean("Mode","debugMode")

# MotionSensor class is useful for this target
ms = MotionSensor(18)
# WaterPomp
waterPomp = OutputDevice(17)

# Main program loop
while True:
  if ms.motion_detected:
      if debugMode:
        print("on")
      else:
        waterPomp.on()
      time.sleep(3)
  else:
      if debugMode:
        print("OFF")
      else:
        waterPomp.off()
