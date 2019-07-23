#!/usr/bin/env python3.7

from pad4pi import rpi_gpio
import time

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
loop_bool = True

class KeyStore:
	def __init__(self):
		# Empty list to store characters
		self.pressed_keys = []

	def store_key(self, key):
		if(key=='#'):
			print(self.pressed_keys)
			self.clear_keys()
		else:
			print(key)
			self.pressed_keys.append(key)

	def clear_keys(self):
		self.pressed_keys.clear()

#def printKey(key):
#    print(key)

keys = KeyStore()

# printKey will be called each time a keypad button is pressed
keypad.registerKeyPressHandler(keys.store_key)

print("Hello Max\n")

while(loop_bool):
	time.sleep(0.2)

keypad.cleanup()
