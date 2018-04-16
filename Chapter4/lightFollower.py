from OmegaExpansion import relayExp
from OmegaExpansion import onionI2C
import time
import sys

if len (sys.argv) != 2:
	print "Need offset"
	exit()

# Initialize relay board
addr = int(sys.argv[1])
relayExp.driverInit(addr)

# Initialize I2C
i2c = onionI2C.OnionI2C()

# Define movement functions
# Relay0 = right motor
# Relay1 = left motor

def turnRight90():
	relayExp.setChannel(addr, 1, 1)
	time.sleep(0.25)
	relayExp.setChannel(addr, 1, 0)
	return

def turnLeft90():
	relayExp.setChannel(addr, 0, 1)
	time.sleep(0.25)
	relayExp.setChannel(addr, 0, 0)
	return

def moveForward():
	relayExp.setAllChannels(addr, 1)
	time.sleep(0.5)
	relayExp.setAllChannels(addr, 0)
	return	

while True:

	# Get values from photoresistors
	# Right Rear = RR
	data = [0xC4, 0x83]
	i2c.writeBytes(0x48, 0x01, data)
	time.sleep(0.5)
	data = i2c.readBytes(0x48, 0x00, 2)
	RR = data[0] * 256 + data[1]
	if RR > 32767:
		RR -= 65535

	# Left Rear = LR
	data = [0xD4, 0x83]
	i2c.writeBytes(0x48, 0x01, data)
	time.sleep(0.5)
	data = i2c.readBytes(0x48, 0x00, 2)
	LR = data[0] * 256 + data[1]
	if LR > 32767:
		LR -= 65535

	# Left Front = LF
	data = [0xE4, 0x83]
	i2c.writeBytes(0x48, 0x01, data)
	time.sleep(0.5)
	data = i2c.readBytes(0x48, 0x00, 2)
	LF = data[0] * 256 + data[1]
	if LF > 32767:
		LF -= 65535

	# Right Front = RF
	data = [0xF4, 0x83]
	i2c.writeBytes(0x48, 0x01, data)
	time.sleep(0.5)
	data = i2c.readBytes(0x48, 0x00, 2)
	RF = data[0] * 256 + data[1]
	if RF > 32767:
		RF -= 65535

	# Determine brightest value
	top = "NONE"

	if LF > RF and LF > LR and LF > RR:
		top = "LF"
	elif RF > LF and RF > LR and RF > RR:
		top = "RF"
	elif LR > LF and LR > RF and LR > RR:
		top = "LR"
	elif RR > LF and RR > RF and RR > LR:
		top = "RR"


	# Determine which way to move
	if top == "RR":
		turnRight90()
		turnRight90()
		moveForward()

	elif top == "RF":
		turnRight90()
		moveForward()

	elif top == "LF":
		turnLeft90()
		moveForward()

	elif top == "LR":
		turnLeft90()
		turnLeft90()
		moveForward()

	else:
		turnLeft90()
		moveForward()


