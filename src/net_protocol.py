#
# This file contains constants for the network protocol
#

# Message header
# | MsgType | MsgLenght | MsgID |
# 2 + 2 + 4 bytes
MSG_HEADER_SIZE = 8

# Maximum message size including 8 byte header
MSG_MAX_SIZE = 4096

# Messages Types
MSGT_GAMESTATE = 2  # message type for game state
MSGT_CONNECTREQ = 3  # connect to server
