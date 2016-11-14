#!/usr/bin/python
# coding=utf-8

from RBClient import *
from Protocol import *
from UdpClient import *
from RBio import *
from RBNetwork import *
from RBHttp import *
from RBMaster import *
from C4Light import *
import logging
import logging.config
import os
import threading

MASTER_AUTHOR = 0x22
SUB_AUTHOR = 0x23

class Business(object):
	def callback(self,data):
		self.logger.info('recv from server : %s' % binascii.b2a_hex(data))
		pro = Protocol.decode(data)

		if (pro.head != 0xEC or pro.tail != 0xEA):
			return
		# 服务器认证
		if (pro.cmd == MASTER_AUTHOR):
			ip = "%d.%d.%d.%d" % (pro.state, pro.R, pro.G, pro.B)
			port = pro.deviceID
			self.client = RBClient(ip, port)
			protocol = Protocol(SUB_AUTHOR, pro.masterID)
			self.client.sendData(protocol.command())
        		self.client.recvData(self.callback)
		# 控制设备
		if (pro.cmd == 0x03):
			light = C4Light()
			if pro.state:
				light.powerOn(pro.deviceID)
			else:
        			light.powerOff(pro.deviceID)

	def broadcast(self):
		UdpClient().broadcast()


	def connect(self, ip, port, masterID):
		client = RBClient(ip, port)

		protocol = Protocol(MASTER_AUTHOR, masterID)
		client.sendData(protocol.command())
		client.recvData(self.callback)


	def main(self):
		# 当前脚本目录
		scriptPath = os.path.split(os.path.realpath(sys.argv[0]))[0]
		logPath = os.path.join(scriptPath, 'logger.conf')

		logging.config.fileConfig(logPath)
		self.logger = logging.getLogger("main")
		configPath = os.path.join(scriptPath, 'RBConfig')
		conf = RBio(configPath)
		ip = conf.getProperty("cloudIP")
		port = int(conf.getProperty("cloudPort"))
    
		master = RBMaster()
		master.ip = conf.getProperty("C4IP", 'C4')
		master.port = int(conf.getProperty("C4Port", 'C4'))

		if conf.hasKey("masterID"):
			masterID = conf.getProperty("masterID")
		else:
			host = conf.getProperty("httpHost")
			httpPort = conf.getProperty("httpPort")

			data = master.toJson()
		        url = "http://%s:%s/Cloud/host_config_upload.aspx" % (host, httpPort)
		        param = {'optype': 1, 'jsondata': data}
		        http = RBHttp(url, param)
		        masterID = http.uploadInfo()
		        if masterID:
		        	conf.writeProperty("masterID", masterID)
		        else:
				self.logger.error('upload error.')
				return

		threads = []
		t1 = threading.Thread(target=self.broadcast)
		threads.append(t1)
		t2 = threading.Thread(target=self.connect, args=(ip, port, int(masterID,16)))
		threads.append(t2)

		for t in threads:
			t.setDaemon(True)
			t.start()

		t.join()

if __name__ == '__main__':
	business=Business()
	RBNetwork().check(business.main)
