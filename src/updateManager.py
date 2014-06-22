import sys
from player import Player, Direction, Position
from event_manager import EventManager, EVENT_TYPE_PLAYER_MOVE, EVENT_TYPE_PLAYER_REDIRECT

class UpdateManager(object):
    """updates the game"""
    def __init__(self, eventManager):
        self.eMngr = eventManager 
        pass

    def updateGame(self, game):
        # TODO: restrict move to field size and players around
        if self.eMngr.existEvent(EVENT_TYPE_PLAYER_MOVE):
            player = game.ownPlayer
            event = self.eMngr.getEvent(EVENT_TYPE_PLAYER_MOVE)
            if event.type == EVENT_TYPE_PLAYER_MOVE:
                event.player.currentPos.applyMove(event.move)
            elif event.type == EVENT_TYPE_PLAYER_REDIRECT:
                pass

    def start(self):
        pass

    def stop(self):
        pass
