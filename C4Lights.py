'''
Author: sapatel91
Date: March 2, 2014
File: lightsControl4.py

Purpose: Set or get Control4 light intensity

Disclaimer: USE AT YOUR RISK, I TAKE NO RESPONSIBILITY
            Most likely there won't be any though
'''
import socket
from bs4 import BeautifulSoup

BUFFER_SIZE = 8192

class Light:
	def __init__(self,ip,port):
		self.ip = ip
		self.port = int(port)

	'''
	Sets intensity of dimmer switch
	Parameters: 
	id - Device ID
	value - 0 to 100
	'''
	def setLevel(self, id, value):
		directorConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		directorConn.connect((self.ip,self.port))
		MESSAGE = '<c4soap name="SendToDeviceAsync" async="1"><param name="data" type="STRING"><devicecommand><command>SET_LEVEL</command><params><param><name>LEVEL</name><value type="INT"><static>%d</static></value></param></params></devicecommand></param><param name="idDevice" type="INT">%d</param></c4soap>' % (value, id)
		directorConn.sendall(MESSAGE + "\0")
		directorConn.close()

	'''
	Ramps to a specified level in milliseconds
	Parameters:
		id - Device ID
		percent - Intensity
		time - Duration in milliseconds
	'''
	def rampToLevel(self, id, percent, time):
		directorConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		directorConn.connect((self.ip,self.port))
		MESSAGE = '<c4soap name="SendToDeviceAsync" async="1"><param name="data" type="STRING"><devicecommand><command>RAMP_TO_LEVEL</command><params><param><name>TIME</name><value type="INTEGER"><static>%d</static></value></param><param><name>LEVEL</name><value type="PERCENT"><static>%d</static></value></param></params></devicecommand></param><param name="idDevice" type="INT">%d</param></c4soap>' % (time, percent, id)
		directorConn.sendall(MESSAGE + "\0")
		directorConn.close()
    
	'''
	Returns the light level for a dimmer. Value between 0 and 100.
	NOTE: will return an error if used on light switches use getLightState instead
	'''
	def getLevel(self, id):
		directorConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		directorConn.connect((self.ip,self.port))
		MESSAGE = '<c4soap name="GetVariable" async="False"><param name = "iddevice" type = "INT">%d</param><param name = "idvariable" type = "INT">1001</param></c4soap>' % (id)
		directorConn.sendall(MESSAGE + "\0")
		data = directorConn.recv(BUFFER_SIZE)
		directorConn.close()
		data = BeautifulSoup(data, "html.parser")
		value = data.find("variable")
		value = data.findAll(text=True)
		value = ''.join(value)
		return value

	'''
	Returns the light state. Output is 0 or 1.
	'''
	def getLightState(self, id):
		directorConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		directorConn.connect((self.ip,self.port))
		MESSAGE = '<c4soap name="GetVariable" async="False"><param name = "iddevice" type = "INT">%d</param><param name = "idvariable" type = "INT">1000</param></c4soap>' % (id)
		directorConn.sendall(MESSAGE + "\0")
		data = directorConn.recv(BUFFER_SIZE)
		directorConn.close()
		data = BeautifulSoup(data, "html.parser")
		value = data.find("variable")
		value = data.findAll(text=True)
		value = ''.join(value)
		return value

	def toogle(self, id):
		if(int(self.getLightState(id).strip('\0'))):
			self.setLevel(id, 0)
		else:
			self.setLevel(id, 1)

	def powerOff(self, id):
		if(int(self.getLightState(id).strip('\0'))):
			self.setLevel(id, 0)

	def powerOn(self, id):
		self.setLevel(id, 1)
		
#if __name__ == '__main__':
	#light = Light('192.168.199.228',5020)
	#light.powerOff(63)
