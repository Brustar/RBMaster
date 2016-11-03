from bs4 import BeautifulSoup
import socket
import json
from RBio import *

# Insert the IP of your Control4 system here. Can be obtained from Composer.
BUFFER_SIZE = 8192

def singleton(cls, *args, **kw):
    instances = {}  
    def _singleton():
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton  
 
@singleton  
class RBMaster(object):  
    def __init__(self):
        self.ip = ""
        self.port = 0

    # Connect to Director and issue soap command to get all items on system.
    def queryInfo(self):
        directorConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        directorConn.connect((self.ip,self.port))
        MESSAGE = '<c4soap name="GetItems" async="False"><param name="filter" type="number">0</param></c4soap>'
        directorConn.sendall(MESSAGE + "\0") # The null terminating character is VERY important to include
        data = ""
        out_string = ""
        while not '</c4soap>' in data:
            data = directorConn.recv(BUFFER_SIZE)
            out_string += data
            if '</c4soap>' in data:
                break
        soapData = BeautifulSoup(out_string.decode('ascii', 'ignore'), "html.parser")
        directorConn.close()
        self.data = soapData

    def toJson(self):
        self.queryInfo()
        items = self.data.findAll('item')
        rooms = []
        devices = []
        for item in items:
            if self.getText(item, "type") == "8":
                room = (self.getText(item, "id"), self.getText(item, "name"))
                rooms.append(room)

            if self.getText(item, "type") == "7":
                device = (self.getText(item, "id"), self.getText(item, "name"))
                devices.append(device)
        self.rooms=rooms
        self.device=devices
        return "{'device'=%s,'rooms'=%s}" % (json.dumps(devices),json.dumps(rooms))

    def getText(self,soupData,tag):
        tag = soupData.find(tag)
        try:
            text_parts = tag.findAll(text=True)
            text = ''.join(text_parts)
            return text.strip()
        except:
            return "Value not found!"


'''
if __name__ == '__main__':
    conf = RBio("RBConfig")

    master=RBMaster()
    master.ip = conf.getProperty("C4IP", 'C4')
    master.port = int(conf.getProperty("C4Port", 'C4'))
    print master.toJson()

    f = file("soap", "a+")
    f.write(master.data.__str__())
    f.close()
'''