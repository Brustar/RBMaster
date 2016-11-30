import serial
import binascii
from time import sleep

class RBHardware(object):
	def __init__(self):
		self.serial = serial.Serial('/dev/tty.usbserial', 9600, timeout=0.5)

	def recv(self,length):
		while True:
			data = self.serial.read(length)
			if data == '':
				continue
			else:
				break
			sleep(0.02)
		return data

	def readElectricity(self):
		return self.recv(8)

	def switchAircon(self,data):
		if self.serial.isOpen():
			self.serial.write(data)

	def close(self):
		self.serial.close()


if __name__ == "__main__":
	cmds = ["F501FFFE006400A9", "F501FFFE016400A8" , "F501FFFE026400A7","f501fffe0b64009e","f501fffe046400a5","f501fffe036400a6"]
	hardware = RBHardware()
	for i in range(0 , 20):
		for cmd in cmds:
			hardware.switchAircon(binascii.unhexlify(cmd))
			sleep(0.1)
	readcmd = hardware.readElectricity()
	print binascii.b2a_hex(readcmd)
	hardware.close()
