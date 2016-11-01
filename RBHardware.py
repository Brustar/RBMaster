import serial
from time import sleep

class RBHardware:
	def __init__(self):
		self.serial = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5)

	def recv(self,length):
		data
		while True:
			data = self.serial.read(length)
			if data == '':
				continue
			else:
				break
			sleep(0.02)
		return data

	def readEclectricity(self):
		return self.recv(20)

	def switchAircon(self,data):
		self.serial.write(data)
