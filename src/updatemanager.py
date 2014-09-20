import sys
from player import Player, Position
from direction import Direction
from eventmanager import EventManager, EVENT_TYPE_PLAYER_MOVE, EVENT_TYPE_PLAYER_REDIRECT, EventSubscriber

class UpdateManager(EventSubscriber):
    """updates the game"""
    def __init__(self, eventManager):
        self.eMngr = eventManager 
        eventManager.subscribe(EVENT_TYPE_PLAYER_MOVE, self)
        eventManager.subscribe(EVENT_TYPE_PLAYER_REDIRECT, self)
        pass

    def updateGame(self, game):
        # think if there is something to be done here. all should be onEvent instead?
         pass

    def onEvent(self, etype, event):
        if (etype == EVENT_TYPE_PLAYER_MOVE):
            event.player.currentPos.applyMove(event.move)
        elif (etype == EVENT_TYPE_PLAYER_MOVE):
            event.player.currentDir = event.direction

    def start(self):
        pass

    def stop(self):
        pass
