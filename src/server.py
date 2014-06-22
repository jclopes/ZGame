#! /usr/bin/env python

import sys
import socket
import select
import struct
import time

from clock import Clock
from net_protocol import MSG_HEADER_SIZE
from net_protocol import MSGT_CONNECTREQ, MSGT_HEARTBEAT
from net_protocol import message_accept, message_state
from net_protocol import unpack_header, receive_msg


HOST = '0.0.0.0'
PORT = 2048

FRAMETIME = 0.06666  # 1/15 seconds
MAX_CLIENTS = 10


class ClientProxy():
    def __init__(self, cliAddr, cliId):
        self.addr = cliAddr
        self.cliId = cliId
        self.srvPort = PORT+cliId
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((HOST, self.srvPort))
        self.sock.setblocking(0)
        self.msgId = 0
        self.lastHbt = 0
        self.lag = 0
        self.msg_metrics = {}  # keep track of RoudTripTime

    def send_state(self, data):
        self.msgId += 1
        msg = message_state(self.msgId, data)
        self.sock.sendto(msg, self.addr)
        # store send time to mesure lag
        self.msg_metrics[self.msgId] = time.time()

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
                    self.mesure_lag(msgId)

    def mesure_lag(msgId):
        t1 = time.time()
        if msgId in self.msg_metrics:
            self.lag = t1 - self.msg_metrics.pop(msgId)

    def is_alive(self):
        return (self.msgId - self.lastHbt) < 10

    def disconnect(self):
        self.sock.close()


class ClientManager(object):
    def __init__(self):
        """Initializes the ClientManager.
        Creates the socket where clients will send request for connection.
        """
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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((HOST, PORT))
        self.sock.setblocking(0)

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

    def receive_connections(self):
        buff = None
        buff, addr = receive_msg(self.sock)
        if buff is not None:
            header = buff[:MSG_HEADER_SIZE]
            data = buff[MSG_HEADER_SIZE:]
            protoVerId, msgType, msgId = struct.unpack('!BBH', header)

            if msgType == MSGT_CONNECTREQ:
                print "connection request from: %s" % (addr,)
                cliId = self.insert(addr)
                cli = self.get_cli(cliId)
                cli.send_accept()

    def read_incoming_msgs(self, timeout):
        rfd_set = [self.sock]
        for c in self.clients:
            cli = self.get_cli(c)
            if cli is not None:
                rfd_set.append(cli.sock)
        t0 = time.time()
        while timeout > 0:
            r, w, x = select.select(rfd_set, [], [], timeout)
            self.read_clients()
            if self.sock in r:
                self.receive_connections()
            timeout -= (time.time() - t0)


def main():
    cliMngr = ClientManager()
    clock = Clock(FRAMETIME)

    clock.start()
    while True:
        state = '{"team":[[10,10]],[[10,20]]}'
        # check if there are new clients trying to conect
        cliMngr.receive_connections()
        # send game state to all clients
        cliMngr.broadcast(state)
        # read clients input while we can
        timeout = clock.sleep_time()
        cliMngr.read_incoming_msgs(timeout)
        # drop clients that are not responsive
        cliMngr.check_clients_liveness()

        clock.sleep()


if __name__ == '__main__':
    sys.exit(main())
