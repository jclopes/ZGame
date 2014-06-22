import sys
from player import Player, Direction, Position
from event_manager import EventManager, EVENT_SET_PLAYER, EVENT_TYPE_PLAYER_MOVE, EVENT_TYPE_PLAYER_REDIRECT

class UpdateManager(object):
    """updates the game"""
    def __init__(self, eventManager):
        self.eMngr = eventManager 
        pass

    def updateGame(self, game):
        # TODO: restrict move to field size and players around

        # treat the player events
        while self.eMngr.existEvent(EVENT_SET_PLAYER):
            player = game.ownPlayer
            event = self.eMngr.getEvent(EVENT_SET_PLAYER)
            if event.type == EVENT_TYPE_PLAYER_MOVE:
                event.player.currentPos.applyMove(event.move)
            elif event.type == EVENT_TYPE_PLAYER_REDIRECT:
                pass

    def start(self):
        pass

    def stop(self):
        pass
