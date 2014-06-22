#! /usr/bin/env python

import sys
import socket
import struct

from net_protocol import MSG_HEADER_SIZE, MSG_MAX_SIZE
from net_protocol import MSGT_GAMESTATE, MSGT_CONNECTACPT
from net_protocol import message_connect, message_heartbeat


def main(srvAddr, srvPort):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = message_connect()
    s.sendto(msg, (srvAddr, srvPort))

    msgCounter = 1
    while True:
        buff, addr = s.recvfrom(MSG_MAX_SIZE)
        header = buff[:MSG_HEADER_SIZE]
        data = buff[MSG_HEADER_SIZE:]
        protoVerId, msgType, msgId = struct.unpack('!BBH', header)
        if msgId > msgCounter:
            print "package loss: %s" % (msgId - msgCounter)
            print msgId
            print msgCounter
        msgCounter = msgId+1
        if msgType == MSGT_CONNECTACPT:
            (_newSrvAddr, srvPort) = addr
            print "updated server port to: %s" % srvPort
        if msgType == MSGT_GAMESTATE:
            print data
            msg = message_heartbeat(msgId)
            s.sendto(msg, (srvAddr, srvPort))
            print "sent heartbeat"

        else:
            print "Unknown message type!"
            print protoVerId
            print msgType
            print msgId
            print buff


if __name__ == '__main__':
    srvAddr = sys.argv[1]
    srvPort = int(sys.argv[2])
    sys.exit(main(srvAddr, srvPort))
