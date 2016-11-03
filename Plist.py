from biplist import *
import logging

class Plist(object):
	def __init__(self,plistPath):
		try:
			self.plist = readPlist(plistPath)
		except (InvalidPlistException, NotBinaryPlistException), e:
				logger = logging.getLogger("client")
				logger.error("Not a plist:", e)
		

	def property(self,key):
		return self.plist[key]

	def devices(self):
		return self.plist.devices

	def schedules(self):
		return self.plist.schedules

'''
if __name__ == '__main__':
	p=Plist('/Users/Brustar/Downloads/00FF_183.plist')
	print p.property('sceneID')
	print p.devices()
	print p.schedules()

	data={'a':'woo','b':"hi",'c':900}
	writePlist(data,'abc.plist',False)
'''
