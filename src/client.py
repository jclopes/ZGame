#! /usr/bin/env python

import sys
import socket
import struct

from net_protocol import MSG_HEADER_SIZE, MSG_MAX_SIZE
from net_protocol import MSGT_CONNECTREQ, MSGT_GAMESTATE


def main(srvAddr, srvPort):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = bytearray()
    msg.extend(struct.pack('!HHI', MSGT_CONNECTREQ, 0, 0))
    s.sendto(msg, (srvAddr, srvPort))

    while True:
        buff, addr = s.recvfrom(MSG_MAX_SIZE)
        header = buff[:MSG_HEADER_SIZE]
        data = buff[MSG_HEADER_SIZE:]
        msgType, lenght, msgId = struct.unpack('!HHI', header)
        if msgType == MSGT_GAMESTATE:
            print data
        else:
            print "Unknown message type!"
            print msgType
            print lenght
            print msgId
            print buff


if __name__ == '__main__':
    srvAddr = sys.argv[1]
    srvPort = int(sys.argv[2])
    sys.exit(main(srvAddr, srvPort))
