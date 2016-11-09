#!/usr/bin/python
# coding=utf-8

from RBClient import *
from Protocol import *
from UdpClient import *
from RBio import *
import logging
import logging.config
import os
import threading

MASTER_AUTHOR = 0x22
SUB_AUTHOR = 0x23


def callback(data):
    logger = logging.getLogger("main")
    logger.info('recv from server : %s' % binascii.b2a_hex(data))
    pro = Protocol.decode(data)

    if (pro.head != 0xEC or pro.tail != 0xEA):
        return
    # 服务器认证
    if (pro.cmd == MASTER_AUTHOR):
        ip = "%d.%d.%d.%d" % (pro.state, pro.R, pro.G, pro.B)
        port = pro.deviceID
        client = RBClient(ip, port)
        protocol = Protocol(SUB_AUTHOR, 0x00FF)
        client.sendData(protocol.command())
        client.recvData(callback)
    # 控制设备
    if (pro.cmd == 0x03):
        pass


def broadcast():
    UdpClient().broadcast()


def connect(ip, port):
    client = RBClient(ip, port)
    protocol = Protocol(MASTER_AUTHOR, 0x00FF)
    client.sendData(protocol.command())
    client.recvData(callback)


if __name__ == '__main__':
    threads = []
    t1 = threading.Thread(target=broadcast)
    threads.append(t1)

    # 当前脚本目录
    scriptPath = os.path.split(os.path.realpath(sys.argv[0]))[0]
    logPath = os.path.join(scriptPath, 'logger.conf')

    logging.config.fileConfig(logPath)
    configPath = os.path.join(scriptPath, 'RBConfig')
    conf = RBio(configPath)
    ip = conf.getProperty("cloudIP")
    port = int(conf.getProperty("cloudPort"))

    # conf.writeProperty("abc",123)
    t2 = threading.Thread(target=connect, args=(ip, port))
    threads.append(t2)

    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()
