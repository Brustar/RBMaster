import ConfigParser

DEFAULT_SECTION = "server"

class RBio(object):
	def __init__(self,filePath):
		self.confPath=filePath
		self.cf = ConfigParser.ConfigParser()
		self.cf.read(filePath)

	def hasKey(self,key,section = DEFAULT_SECTION):
		return self.cf.has_option(section,key)

	def getProperty(self,key,section = DEFAULT_SECTION):
		return self.cf.get(section, key)

	def writeProperty(self,key,value,section = DEFAULT_SECTION):
		self.cf.set(section, key, value)
		self.cf.write(open(self.confPath, "w"))
