import sys
from player import Player, Direction, Position

class UpdateManager(object):
    """updates the game"""
    def __init__(self):
        pass

    def updateGame(self, game):
        # TODO: restrict move to field size and players around
        player = game.ownPlayer
        if player.proposedMove != None: #TODO pass to event
            player.currentPos.applyMove(player.proposedMove)
            player.proposedMove = None

    def start(self):
        pass

    def stop(self):
        pass
