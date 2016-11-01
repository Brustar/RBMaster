#!/usr/bin/python
#coding=utf-8

from RBClient import *
from Protocol import *
from RBio import *

def callback(data):
	pro=Protocol.decode(data)
	print "recv: cmd= %2x,masterID = %4x,state = %2x,R=%2x,G=%2x,B=%2x,deviceID=%4x,deviceType=%2x" %(pro.cmd,pro.masterID,pro.state,pro.R,pro.G,pro.B,pro.deviceID,pro.deviceType)
	
	if(pro.head!=0xEC or pro.tail!=0xEA):
		return

	if(pro.cmd==0x82):
		ip= "%d.%d.%d.%d" % (pro.state,pro.R,pro.G,pro.B)
		port=pro.deviceID
		client = RBClient(ip,port)
		client.sendData('aaaa')
	

if __name__ == '__main__':
	#client = RBClient('localhost',8080)
	conf=RBio("RBConfig")
	ip = conf.getProperty("cloudIP")
	port = conf.getProperty("cloudPort")
	
	#conf.writeProperty("abc",123)
	client = RBClient(ip,int(port))
	protocol=Protocol(0x82,0x00ff);
	client.sendData(protocol.command())
	client.recvData(callback)
