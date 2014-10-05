import json
import logging

from eventmanager import EventSubscriber, EventClassNetwork, EventClassInput
from eventmanager import EVENT_CLASS_NETWORK, EVENT_CLASS_INPUT

from net_protocol import MSGT_GAMESTATE, MSGT_CONNECTACPT
from net_protocol import cli_recv, cli_connect_req, cli_socket, cli_send
from net_protocol import message_action, message_heartbeat


log = logging.getLogger('ZGame.cli')

class NetworkManager(EventSubscriber):
    """Implements the network protocol.
    Submits player input to server.
    Receives game state from the server.
    """
    STATE_DISCONNECTED = 0
    STATE_CONNECTED = 1
    STATE_CONN_WAIT = 2

    REQ_TIMEOUT_MS = 0.1
    HEARTBEAT_INTERVAL = 0.5  # seconds

    def __init__(self, eventManager, world):
        super(NetworkManager, self).__init__()
        self.eMngr = eventManager
        self.state = self.STATE_DISCONNECTED
        self.conn_retries = 5
        self.sock = cli_socket()
        self.msgCounter = 1
        self.srvAddr = None
        self.timePassed = 0.0  # Time passed waiting for a reply
        self.heartbeatTimer = 0.0  # Time passed since last message was sent

    def update(self, timeDelta):
        self.timePassed += timeDelta
        self.heartbeatTimer += timeDelta

        if self.state == self.STATE_DISCONNECTED:
            log.info("NM: ERROR: No connection to Server. need to call start().")

        if self.state == self.STATE_CONN_WAIT:
            self._update_conn_wait()

        elif self.state == self.STATE_CONNECTED:
            self._update_connected()

    def _update_conn_wait(self):
        msg = cli_recv(self.sock)
        if msg is None:
            if self.timePassed > self.REQ_TIMEOUT_MS:
                if self.conn_retries == 0:
                    raise Exception('CRITICAL: Server not responding.')
                log.info("NM: retrying connection.")
                cli_connect_req(self.sock, self.srvAddr)
                self.timePassed = 0
                self.conn_retries -= 1
        elif msg['type'] == MSGT_CONNECTACPT:
            log.info("NM: Connected to server.")
            self.srvAddr = msg['addr']
            self.timePassed = 0
            self.state = self.STATE_CONNECTED
            connectedEvent = EventClassNetwork(
                EventClassNetwork.TYPE_CONNECTED, None
            )
            self.eMngr.publishEvent(connectedEvent)
        else:
            log.info("NM: ERROR: unexpected message.")

    def _update_connected(self):
        self.processEvents()
        # Get all messages from the server
        msg = cli_recv(self.sock)
        while (msg is not None):
            if msg['type'] == MSGT_GAMESTATE:
                # TODO: umpack world state and events
                if msg['id'] > self.msgCounter + 1:
                    # Not the message we were expecting
                    # TODO: use logging
                    log.info("NM: WANING: package loss: %s" % (msg['id'] - self.msgCounter))
                # update message counter
                self.msgCounter = msg['id']
                self.timePassed = 0
                log.debug("%s" % msg)
                # TODO: Process server message
                # TODO: emit events to update world and event queue
            # Get the next message
            msg = cli_recv(self.sock)

    def processEvents(self):
        """Processes the events in FIFO order."""
        msgQueue = list()
        while(len(self.eQueue) > 0):
            event = self.eQueue.pop(0)
            if event.eclass != EVENT_CLASS_INPUT:
                log.info("NM: WANING: Unexpected event.")
            else:
                msgQueue.append(event.properties)

        if (len(msgQueue) > 0):
            payload = json.dumps(msgQueue)
            msg = message_action(self.msgCounter, payload)
            res = cli_send(self.sock, msg, self.srvAddr)
            log.info("NM: send action. msgId=%s. %s" % (self.msgCounter, res))
        else:
            msg = message_heartbeat(self.msgCounter)
            res = cli_send(self.sock, msg, self.srvAddr)

            log.info("NM: send HeartBeat. msgId=%s addr=%s. %s" % (self.msgCounter, self.srvAddr, res))

    def start(self, srvHost, srvPort):
        self.srvAddr = (srvAddr, srvPort)
        cli_connect_req(self.sock, self.srvAddr)
        self.msgCounter = 1
        self.state = self.STATE_CONN_WAIT
        self.eMngr.subscribe(EVENT_CLASS_INPUT, self)

    def stop(self):
        # TODO: send disconnect
        pass


## TESTING CODE ## ============================================================
import sys
from eventmanager import EventManager
from clock import Clock


def main(srvHost, srvPort):
    logHandler = logging.StreamHandler(stream=sys.stderr)
    log.addHandler(logHandler)
    log.setLevel(logging.DEBUG)
    log.info('Start testing NetworkManager.')

    w = dict()
    em = EventManager()
    nm = NetworkManager(em, w)
    FRAME_TIME = 0.2  # seconds
    c = Clock(FRAME_TIME)
    c.start()
    slept_time = 0.0
    nm.start(srvHost, srvPort)
    counter = 30
    exit = False
    while not exit:
        nm.update(slept_time + c.time_passed())

        counter -= 1
        if counter <= 0:
            exit = True

        if counter == 10:
            em.publishEvent(
                EventClassInput(
                    EventClassInput.TYPE_SPEED,
                    {"player": 1, "speed": 1}
                )
            )
        slept_time = c.time_left()
        c.sleep()
        # log.debug("%s" % (counter * FRAME_TIME))


if __name__ == '__main__':
    srvAddr = sys.argv[1]
    srvPort = int(sys.argv[2])
    sys.exit(main(srvAddr, srvPort))
