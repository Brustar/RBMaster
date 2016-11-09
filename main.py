#!/usr/bin/python
#coding=utf-8

from RBClient import *
from Protocol import *
from UdpClient import *
from RBio import *
import logging
import logging.config
import os

MASTER_AUTHOR = 0x22
SUB_AUTHOR = 0x23

def callback(data):
	logger = logging.getLogger("main")
	logger.info('recv from server : %s' % binascii.b2a_hex(data))
	pro=Protocol.decode(data)

	if(pro.head!=0xEC or pro.tail!=0xEA):
		return
	#服务器认证
	if(pro.cmd==MASTER_AUTHOR):
		ip= "%d.%d.%d.%d" % (pro.state,pro.R,pro.G,pro.B)
		port=pro.deviceID
		client = RBClient(ip,port)
		protocol = Protocol(SUB_AUTHOR, 0x00A8)
		client.sendData(protocol.command())
		client.recvData(callback)
	#控制设备
	if(pro.cmd==0x03):
		pass
	

if __name__ == '__main__':
	#UdpClient().broadcast()
	#当前脚本目录
	scriptPath = os.path.split(os.path.realpath(sys.argv[0]))[0]
	logPath = os.path.join(scriptPath,'logger.conf')
	print logPath
	logging.config.fileConfig(logPath)
	configPath= os.path.join(scriptPath,'RBConfig')
	conf=RBio(configPath)
	ip = conf.getProperty("cloudIP")
	port = conf.getProperty("cloudPort")
	
	#conf.writeProperty("abc",123)
	client = RBClient(ip,int(port))
	protocol=Protocol(MASTER_AUTHOR,0x00A8)
	client.sendData(protocol.command())
	client.recvData(callback)
