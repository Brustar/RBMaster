from socket import *  
import time
 
HOST = '<broadcast>'  
PORT = 40000
BUFSIZE = 1024  
ADDR = (HOST, PORT)  

class UdpClient(object):
	def __init__(self):
		self.sock = socket(AF_INET, SOCK_DGRAM)
		
  
	def ip_address(self): 
		try:
			self.sock.connect(('8.8.8.8', 80))
			(addr, port) = self.sock.getsockname()
			return addr
			self.sock.close()
		except socket.error:
			return "127.0.0.1"
 
	def sendnow(self): 
		data = self.ip_address()
		self.sock = socket(AF_INET, SOCK_DGRAM)
		self.sock.bind(('', 0))  
		self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  

		while True:  
			print "sending ->",data  
			self.sock.sendto(data,ADDR)  
			time.sleep(5)
  
		self.sock.close() 

'''
if __name__ == '__main__':
	UdpClient().sendnow()
'''
