#! /usr/bin/env python

import sys
import socket
import struct

from clock import Clock
from net_protocol import MSG_HEADER_SIZE, MSG_MAX_SIZE
from net_protocol import MSGT_CONNECTREQ, MSGT_GAMESTATE, MSGT_HEARTBEAT
from net_protocol import message_accept, message_state
from net_protocol import unpack_header, receive_msg


HOST = ''
PORT = 2048

FRAMETIME = 0.06666  # 1/15 seconds
MAX_CLIENTS = 10


class ClientProxy():
    def __init__(self, cliAddr, cliId):
        self.srvPort = PORT+cliId
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((HOST, self.srvPort))
        s.setblocking(0)
        self.cliId = cliId
        self.sock = s
        self.addr = cliAddr
        self.msgId = 0
        self.lastHbt = 0

    def send_state(self, data):
        self.msgId += 1
        msg = message_state(self.msgId, data)
        self.sock.sendto(msg, self.addr)

    def send_accept(self):
        msg = message_accept(self.srvPort)
        self.sock.sendto(msg, self.addr)

    def receive(self):
        while True:
            buff, addr = receive_msg(self.sock, self.addr)
            print "receive msg: addr=%s buff=%s" % (buff, addr)
            if addr is None:
                break
            if (addr != self.addr):
                print "Wrong address!"
                break
            else:
                msgType, msgId = unpack_header(buff)
                if msgType == MSGT_HEARTBEAT:
                    self.lastHbt = msgId

    def is_alive(self):
        return (self.msgId - self.lastHbt) < 10

    def disconnect(self):
        self.sock.close()


class ClientManager(object):
    def __init__(self):
        self.clients = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
            10: None
        }

    def get_free_slot(self):
        """Return index for a free client slot or 'None'."""
        res = None
        for i in self.clients:
            if self.clients[i] is None:
                res = i
                break
        return res

    def get_cli(self, cliId):
        return self.clients[cliId]

    def insert(self, address):
        """Returns 'None' or the id of the new inserted client."""
        # Check if the client is already connected
        for c in self.clients:
            cli = self.get_cli(c)
            if cli is not None:
                if cli.addr == address:
                    print "reconnect request from %s." % address
                    return c

        cliId = self.get_free_slot()
        if cliId is not None:
            self.clients[cliId] = ClientProxy(address, cliId)
        return cliId

    def remove(self, cliId):
        cli = self.clients[cliId]
        cli.disconnect()
        self.clients[cliId] = None

    def check_clients_liveness(self):
        """Check if the clients are responsive."""
        for c in self.clients:
            cli = self.get_cli(c)
            if cli is not None:
                if not cli.is_alive():
                    print "Lost client %s" % c
                    self.remove(c)

    def broadcast(self, state):
        """Sends a message to all connected clients."""
        for c in self.clients:
            cli = self.get_cli(c)
            if cli is not None:
                cli.send_state(state)

    def read_clients(self):
        """Read input from all connected clients."""
        for c in self.clients:
            cli = self.get_cli(c)
            if cli is not None:
                cli.receive()


def main():
    cliMngr = ClientManager()
    clock = Clock(FRAMETIME)

    # Send a message every 1/20 seconds
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    s.setblocking(0)

    clock.start()
    while True:
        state = '{"team":[[10,10]],[[10,20]]}'
        buff = None
        try:
            buff, addr = s.recvfrom(MSG_MAX_SIZE)
        except socket.error as e:
            if e.errno != 35:  # ignore "Resource temporarily unavailable"
                raise

        if buff is not None:
            header = buff[:MSG_HEADER_SIZE]
            data = buff[MSG_HEADER_SIZE:]
            protoVerId, msgType, msgId = struct.unpack('!BBH', header)

            if msgType == MSGT_CONNECTREQ:
                print "connection request from: %s" % (addr,)
                cliId = cliMngr.insert(addr)
                cli = cliMngr.get_cli(cliId)
                cli.send_accept()

        cliMngr.broadcast(state)
        cliMngr.read_clients()
        cliMngr.check_clients_liveness()

        clock.sleep()


if __name__ == '__main__':
    sys.exit(main())
