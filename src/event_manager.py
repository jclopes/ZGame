import sys
from player import Player


EVENT_TYPE_PLAYER_MOVE = 0
EVENT_TYPE_PLAYER_REDIRECT = 1
EVENT_TYPE_GAME_CLOSE = 2
EVENT_TYPES = [EVENT_TYPE_PLAYER_MOVE, EVENT_TYPE_PLAYER_REDIRECT, EVENT_TYPE_GAME_CLOSE]


class EventManager(object):
    """handles the events between managers in the game"""


    def __init__(self):
        self.playerEvents = []
        self.gameEvents = []
        self.eventQueue = {
                EVENT_TYPE_PLAYER_MOVE : self.playerEvents,
                EVENT_TYPE_PLAYER_REDIRECT : self.playerEvents,
                EVENT_TYPE_GAME_CLOSE : self.gameEvents
        }

    def addEvent(self, event):
        self.eventQueue[event.type].append(event)

    def getEvent(self, etype):
        return self.eventQueue[etype].pop(0)

    def getEvents(self, etype):
        #TODO returns the list right now
        return self.eventQueue[etype]

    def existEvent(self, etype):
        return len(self.eventQueue[etype]) > 0

    def start(self):
        pass

    def stop(self):
        pass


class Event(object):
    """represents an event in the game"""

    def __init__(self, etype):
        self.type = etype


class EventPlayerMove(Event):
    """represents an event for a player moving"""

    def __init__(self, player, move):
        super(EventPlayerMove, self).__init__(EVENT_TYPE_PLAYER_MOVE)
        self.player = player
        self.move = move

