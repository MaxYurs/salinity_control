#!/usr/bin/env python3.7

# ----------------------------------------------------------------------------------- #
#       Adapted from code written by iTechno on the blog post "Interface 16x2         #    
#       Alphanumeric LCD And4x4 Matrix Keypad With Raspberry Pi3"                     #
#-------------------------------------------------------------------------------------#

from pad4pi import rpi_gpio
import time
import RPi.GPIO as GPIO
from uFire_EC import uFire_EC
import Adafruit_CharLCD as LCD
import os.path
from os import path


class KeyStore:
	def __init__(self):
		# Empty list to store characters
		self.pressed_keys = []
		self.salinity = 0
		self.check_salinity = 0
		self.print_salinity = 1
		self.cursor_loc = 1

	def store_key(self, key):
		if(key=='#'):
			self.check_salinity = 1
			lcd.clear()
		elif(key=='A' or key=='B' or key=='C' or key=='D' or key=='*'):
			lcd.clear()
			lcd.message("A, B, C, D, and *\n not implemented yet")
			time.sleep(3)
		else:
			lcd.clear()
			if(self.print_salinity):
				self.print_salinity = 0
			self.pressed_keys.append(key)
			s = [str(i) for i in self.pressed_keys]
			lcd.message("Set to: \n" + ''.join(s) + "%")

	def clear_keys(self):
		self.pressed_keys.clear()

	def get_salinity(self):
		# Check if press_keys is empty
		if len(self.pressed_keys) != 0:
			# Convert integer list into string
			s = [str(i) for i in self.pressed_keys]

			# Join list items using join()
			self.salinity = int("".join(s))
		else:
			print("List is empty, salinity set to default\n")
			self.salinity = 0
		return self.salinity

# Setup keypad
KEYPAD = [
    [1, 2, 3, "A"],
    [4, 5, 6, "B"],
    [7, 8, 9, "C"],
    ["*", 0, "#","D"]
]

ROW_PINS = [24, 22, 27, 18] # BCM numbering
COL_PINS = [17, 15, 14, 4] # BCM numbering

factory = rpi_gpio.KeypadFactory()

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

# ------------------------------------------------------------------------------------#
#                                  LCD Setup                                          #
# ------------------------------------------------------------------------------------#
lcd_rs = 26
lcd_en = 19
lcd_d4 = 13
lcd_d5 = 6
lcd_d6 = 5
lcd_d7 = 11
lcd_backlight = 2

lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# ----------------------------------------------------------------------------------- #
#                              Salinity Variable Def                                  #
# ----------------------------------------------------------------------------------- #
sal_cur     = 0
def_sal     = 50
sal_desired = def_sal
loop_bool   = True

keys = KeyStore()

# keys.store_key will be called each time a keypad button is pressed
keypad.registerKeyPressHandler(keys.store_key)

ec=uFire_EC(i2c_bus=1, address=0x3c)

# ----------------------------------------------------------------------------------- #
#                                 Get Settings                                        #
# ----------------------------------------------------------------------------------- #
if(path.exists('settings.txt'):
   #TODO: Pull default salinity from file "settings.txt" f=open("settings.txt", 

# ----------------------------------------------------------------------------------- #
#                                    Main                                             #
# ----------------------------------------------------------------------------------- #

lcd.clear()
lcd.message("Brine Mixer\nFrost Inc.")
time.sleep(5)

lcd.clear()
lcd.message("Def. salinity:\n" + str(def_sal) + "%")
time.sleep(5)

lcd.clear()
#lcd.message("")
#time.sleep(5)
lcd.clear()

while(loop_bool):
	if(keys.check_salinity):
		if(keys.get_salinity() == 999):
			lcd.clear()
			lcd.message("Goodbye")
			time.sleep(2)
			lcd.clear()
			break
		elif(keys.get_salinity() < 100):
			sal_desired = keys.get_salinity()
			lcd.clear()
			#lcd.message("Sal des: " + str(sal_desired) + "\nSal cur: " + str(sal_cur))
		else:
			lcd.clear()
			lcd.message("Sal > 100 inv\nDef sal used")
			time.sleep(2)
			sal_desired = def_sal

		keys.clear_keys()
		keys.check_salinity = 0
		keys.print_salinity = 1

	ec.measureEC()
	sal_cur=ec.salinityPSU
	#if(sal_desired > sal_cur):
		#SET GPIO HIGH 
	if(keys.print_salinity):
		lcd.clear()
		lcd.message("Sal des: " + str(sal_desired) + "%\nSal cur: " + str(sal_cur) + "%")
	time.sleep(0.2)

keypad.cleanup()
