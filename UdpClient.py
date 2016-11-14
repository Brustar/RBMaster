from socket import *  
from RBNetwork import *
import time
 
HOST = '<broadcast>'  
PORT = 10000
BUFSIZE = 1024  
ADDR = (HOST, PORT)  

class UdpClient(object):
	def __init__(self):
		self.sock = socket(AF_INET, SOCK_DGRAM)
 
	def broadcast(self): 
		network = RBNetwork() 
		data = network.readip()
		self.sock.bind(('', 0))  
		self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  

		while True:  
			print "sending ->",data  
			self.sock.sendto(data,ADDR)  
			time.sleep(5)
  
		self.sock.close() 

'''
if __name__ == '__main__':
	UdpClient().broadcast()
'''
