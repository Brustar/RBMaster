#coding=utf-8
import requests

class RBHttp(object):
	def uploadAllMasterInfo():
		pass

	def readDvices():
		pass

	def readRooms():
		pass

	def readScenes():
		pass

if __name__ == "__main__":
	r = requests.get('http://localhost:3000/msgs')
	print r.text
	print r.encoding
	print r.headers
