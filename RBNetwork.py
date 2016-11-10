import os
import re
import time
import logging
import platform

class RBNetwork(object):
    def readip(self):
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
'''
def handle():
    print 'ok..'

if __name__ == '__main__':
    #RBNetwork().check(handle)
    print RBNetwork().readip()
'''
