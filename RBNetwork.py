import os
import re
import time
import logging
import platform
import commands

class RBNetwork(object):
	def wifi_ip(self):
		cmd='ifconfig en0'
		sysstr = platform.system()
		if sysstr == "Linux":
			cmd='ifconfig wlan0'
		info = os.popen(cmd)
		pattern = '((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))'
		ip = re.search(pattern,info.read())
		if ip:
			return ip.group()
		return ip

	def readip(self):
		cmd = "ifconfig | grep 'inet ' | awk '{print $2}'"
		sysstr = platform.system()
		if sysstr == "Linux":
			cmd="ifconfig | grep 'inet addr' | awk '{print $2}' | awk -F: '{print $2}'"
		(status, output) = commands.getstatusoutput(cmd)
		if status == 0:
			ips = output.split('\n')
			for ip in ips:
				if ip != '127.0.0.1':
					return ip
		return None

	def check(self,handle):
		while True:
			ip = self.readip()
			if ip:
				handle()
				break
			else:
				logger = logging.getLogger("client")
				logger.info('check....')
			time.sleep(2)


#if __name__ == '__main__':
	#print RBNetwork().ip()

