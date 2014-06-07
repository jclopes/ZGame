#! /usr/bin/env python

import sys
import socket
import struct

from clock import Clock
from net_protocol import MSG_HEADER_SIZE, MSG_MAX_SIZE
from net_protocol import MSGT_CONNECTREQ, MSGT_GAMESTATE


HOST = ''
PORT = 2048
FRAMETIME = 0.06666  # 1/15 seconds


class ClientProxy():
    def __init__(self, cliAddr):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setblocking(0)

        self.addr = cliAddr
        self.msgId = 0

    def send(self, data):
        msgType = MSGT_GAMESTATE
        self.msgId += 1
        msg = bytearray()
        msg.extend(struct.pack('!HHI', msgType, len(data), self.msgId))
        msg.extend(data)
        self.s.sendto(msg, self.addr)


def main():
    clients = []
    clock = Clock(FRAMETIME)

    # Send a message every 1/20 seconds
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    s.setblocking(0)

    clock.start()
    while True:
        state = '{"team":[[10,10]],[[10,20]]}'
        try:
            buff, addr = s.recvfrom(MSG_MAX_SIZE)
            header = buff[:MSG_HEADER_SIZE]
            data = buff[MSG_HEADER_SIZE:]
            msgType, lenght, msgId = struct.unpack('!HHI', header)

            if msgType == MSGT_CONNECTREQ:
                clients.append(ClientProxy(addr))
        except socket.error as e:
            if e.errno != 35:  # ignore "Resource temporarily unavailable"
                raise

        for c in clients:
            c.send(state)

        clock.sleep()


if __name__ == '__main__':
    sys.exit(main())
