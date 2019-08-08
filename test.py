#!/usr/bin/env python3.7

from uFire_EC import uFire_EC
import time

ec=uFire_EC(i2c_bus=1, address=0x3c)

while(1):
	ec.measureEC()

	print(str(ec.salinityPSU) + " is the measured salinity cool \n")
	print(str(ec.mS) + " Is that variable idk\n")
	time.sleep(2)

