import ConfigParser

class RBio(object):
	def __init__(self,filePath):
		self.confPath=filePath
		self.cf = ConfigParser.ConfigParser()
		self.cf.read(filePath)

	def getProperty(self,key,section="current"):
		return self.cf.get(section, key)

	def writeProperty(self,key,value,section="current"):
		self.cf.set(section, key, value)
		self.cf.write(open(self.confPath, "w"))