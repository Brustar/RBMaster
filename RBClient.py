import socket
import sys
import time
import binascii

class RBClient(object):
	def __init__(self,ip,port):
		# Create a TCP/IP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bufsize = 1024
		# Connect the socket to the port on the server given by the caller
		server_address = (ip, port)
		self.logger = logging.getLogger("client")

		logger.info('connecting to %s port %s' % server_address)
		self.sock.connect(server_address)

	def sendData(self,message):
		print 'send to server : ' + binascii.b2a_hex(message)
		self.sock.sendall(message)

	def recvData(self,callback):
		while 1:  
			try:  	
				data = self.sock.recv(self.bufsize)  
				time.sleep(0.01)  
				callback(data)

				if not data:  
					break   

			except:  
				self.logger('error.')
				break  

		self.close()
 
	def close(self):
		self.sock.close()
