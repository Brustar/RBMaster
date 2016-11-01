import struct

PATTERN = "!2BH4BH2B"

class Protocol(object):

	def __init__(self,cmd,masterID,state=0,R=0,G=0,B=0,deviceID=0,deviceType=0):
		self.cmd=cmd;
		self.masterID=masterID;
		self.state=state;
		self.R=R
		self.G=G
		self.B=B
		self.deviceID=deviceID
		self.deviceType=deviceType

	def command(self):
		head = 0xEC
		tail = 0xEA 
		return struct.pack(PATTERN, head,self.cmd,self.masterID,self.state,self.R,self.G,self.B,self.deviceID,self.deviceType,tail)

	@staticmethod
	def decode(data):
		head,cmd,masterID,state,R,G,B,deviceID,deviceType,tail=struct.unpack(PATTERN,data)
		pro=Protocol(cmd,masterID,state,R,G,B,deviceID,deviceType)
		pro.head=head
		pro.tail=tail
		return pro
