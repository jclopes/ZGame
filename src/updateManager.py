import sys
from player import Player, Direction, Position

class UpdateManager(object):
    """updates the game"""
    def __init__(self):
        pass

    def updateGame(self, game):
        # TODO: issue. this function can just be used for Game and should be available for other parts as a menu?
        # TODO: restrict move to field size and players around
        player = game.ownPlayer
        if player.proposedPos != None:
            player.updatePosition(player.proposedDir, player.proposedPos)

    def start(self):
        pass

    def stop(self):
        pass
