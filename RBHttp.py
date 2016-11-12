#coding=utf-8
import requests

class RBHttp(object):
	def __init__(self,url,param):
		self.url=url
		self.param=param

	def uploadInfo(self):
		r = requests.post(self.url, data=self.param)
		print r.json()
		if r.json()['Errortype'] == '0' :
			return r.json()['hostid']
		return None

'''
if __name__ == "__main__":
	r = requests.get('http://httpbin.org/get')
	print r.json()['origin']
	print r.encoding
	print r.headers
'''