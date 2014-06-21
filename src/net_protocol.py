import struct
import socket

#
# This file contains constants and message definitions for the network protocol
#

# Protocol Identification
PROTOCOL_ID = 0x50
PROTOCOL_VERSION = 0x01
PROTOCOL_VERSIONID = PROTOCOL_ID + PROTOCOL_VERSION

# Message header
# | PROTOCOL_ID | PROTOCOL_VERSION | MsgType | MsgID |
#   4           + 4                + 8       + 16    = 32 bits
MSG_HEADER_SIZE = 4

# Maximum message size including header (standard size)
MSG_MAX_SIZE = 4096

# Messages Types
MSGT_GAMESTATE = 2  # message type for game state
MSGT_CONNECTREQ = 3  # client request to connect to server
MSGT_CONNECTACPT = 4  # response to client connection request
MSGT_HEARTBEAT = 5  # response to client connection request


def message_accept(srvPort):
    """
    Returns a struct with a ConnectionAccepted message for port 'srvPort'.

    Context: send by the server in response to a connection request.

    This message tells the client that the connection request was accepted
    and which port the client should connect to.
    """
    msg = bytearray()
    # Header
    msg.extend(struct.pack('!BBH', PROTOCOL_VERSIONID, MSGT_CONNECTACPT, 0))
    # Payload
    # TODO: we don't need the payload. UDP header already says the port.
    msg.extend(struct.pack('!H', srvPort))
    return msg


def message_state(msgId, payload):
    msg = bytearray()
    # Header
    msg.extend(struct.pack('!BBH', PROTOCOL_VERSIONID, MSGT_GAMESTATE, msgId))
    # Payload
    msg.extend(payload)
    return msg


def message_connect():
    """Context: sent from the client to request a connection to the server."""
    msg = bytearray()
    # Header
    msg.extend(struct.pack('!BBH', PROTOCOL_VERSIONID, MSGT_CONNECTREQ, 0))
    return msg


def message_heartbeat(msgId):
    """
    Context: sent from the client to the server in regular intervals to keep
    the connection open.
    """
    msg = bytearray()
    # Header
    msg.extend(struct.pack('!BBH', PROTOCOL_VERSIONID, MSGT_HEARTBEAT, msgId))
    return msg


def unpack_header(buff):
    header = buff[:MSG_HEADER_SIZE]
    data = buff[MSG_HEADER_SIZE:]
    protoVerId, msgType, msgId = struct.unpack('!BBH', header)
    return msgType, msgId


def receive_msg(sock, fromAddr=None):
    buff, addr = None, None
    try:
        buff, addr = sock.recvfrom(MSG_MAX_SIZE)
    except socket.error as e:
        if e.errno != 35:  # ignore "Resource temporarily unavailable"
            raise
    # Too short message: discard
    if (buff is not None) and (len(buff) < MSG_HEADER_SIZE):
        return None, None

    return buff, addr
