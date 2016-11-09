import os
import re
import time
import logging

class RBNetwork(object):
    def readip(self):
        info = os.popen('ifconfig en0')
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
    RBNetwork().check(handle)
'''