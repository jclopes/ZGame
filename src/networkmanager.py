from eventmanager import EventSubscriber

from net_protocol import MSGT_GAMESTATE, MSGT_CONNECTACPT
from net_protocol import cli_recv, cli_connect_req, cli_socket


class NetworkManager(EventSubscriber):
    """Implements the network protocol.
    Submits player input to server.
    Receives game state from the server.
    """
    STATE_DISCONNECTED = 0
    STATE_CONNECTED = 1
    STATE_CON_REQUEST = 2

    REQ_TIMEOUT_MS = 0.1

    def __init__(self, eventManager, world):
        self.eMngr = eventManager
        self.state = self.STATE_DISCONNECTED
        self.conn_retries = 5
        self.sock = cli_socket()
        self.msgCounter = 1
        self.srvAddr = None
        self.timePassed = 0.0

    def update(self, timeDelta):
        self.timePassed += timeDelta

        if self.state == self.STATE_DISCONNECTED:
            print "NM: ERROR: No connection to Server. need to call start()."

        if self.state == self.STATE_CON_REQUEST:
            msg = cli_recv(self.sock)
            if msg is None:
                if self.timePassed > self.REQ_TIMEOUT_MS:
                    if self.conn_retries == 0:
                        raise Exception('CRITICAL: Server not responding.')
                    print "NM: retrying connection."
                    cli_connect_req(self.sock, self.srvAddr)
                    self.timePassed = 0
                    self.conn_retries -= 1
            elif msg['type'] == MSGT_CONNECTACPT:
                self.timePassed = 0
                self.state = self.STATE_CONNECTED
                connectedEvent = EventClassNetwork(
                    EventClassNetwork.TYPE_CONNECTED, None
                )
                self.eMngr.publishEvent(connectedEvent)
            else:
                print "NM: ERROR: unexpected message."

        elif self.state == self.STATE_CONNECTED:
            msg = cli_recv(self.sock)
            if msg is None:
                self.timePassed += timeDelta
            elif msg['type'] == MSGT_GAMESTATE:
                # TODO: umpack world state and events
                if msg['id'] > self.msgCounter:
                    # Not the message we were expecting
                    # TODO: use logging
                    print "NM: WANING: package loss: %s" % (msg['id'] - self.msgCounter)
                # update message counter
                self.msgCounter = msg['id'] + 1
                self.timePassed = 0
                print msg
                # TODO: Process server message
                # TODO: update world and event queue

    def start(self, srvHost, srvPort):
        self.srvAddr = (srvAddr, srvPort)
        cli_connect_req(self.sock, self.srvAddr)
        self.msgCounter = 1
        self.state = self.STATE_CON_REQUEST

    def stop(self):
        # TODO: send disconnect
        pass

    def onEvent(self, _eclass, event):
        if self.state != self.STATE_CONNECTED:
            noConnectionEvent = EventClassNetwork(
                EventClassNetwork.TYPE_NO_CONNECTION, None
            )
            self.eMngr.publishEvent(noConnectionEvent)
        else:
            # TODO: process input events and forward them to the server.
            print "NM: received event"


from eventmanager import EventManager
from clock import Clock
def main(srvHost, srvPort):
    w = dict()
    em = EventManager()
    nm = NetworkManager(em, w)
    FRAME_TIME = 0.2  # 200 ms
    c = Clock(FRAME_TIME)
    c.start()
    slept_time = 0.0
    nm.start(srvHost, srvPort)
    counter = 100
    exit = False
    while not exit:
        nm.update(slept_time + c.time_passed())
        counter -= 1
        if counter <= 0:
            exit = True
        slept_time = c.time_left()
        c.sleep()
        print "%s" % (counter * FRAME_TIME)


import sys
if __name__ == '__main__':
    srvAddr = sys.argv[1]
    srvPort = int(sys.argv[2])
    sys.exit(main(srvAddr, srvPort))
