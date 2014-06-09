import sys
import sdl2.ext
from graphicsManager import GraphicManager
from player import Player, Direction, Position

class InputManager(object):
    """processes the user input"""
    def __init__(self, graphicsManager):
        self.gMngr = graphicsManager

    def processUserInput(self, game):
        # TODO: issue. this function can just be used for Game and should be available for other parts as a menu?
        events = sdl2.ext.get_events()
        for event in events:
#            print event.type
            if event.type == sdl2.SDL_QUIT:
                print "QUIT"
                game.isRunning = False
            if event.type == sdl2.SDL_KEYDOWN:
                player = game.ownPlayer
                proposedPos = Position(player.currentPos.x, player.currentPos.y)
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    print "up"
                    proposedPos.moveTo(Direction.UP)
                    player.proposeMove(Direction.UP, proposedPos)
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    print "down"
                    proposedPos.moveTo(Direction.DOWN)
                    player.proposeMove(Direction.DOWN, proposedPos)
                elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                    print "left"
                    proposedPos.moveTo(Direction.LEFT)
                    player.proposeMove(Direction.LEFT, proposedPos)
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    print "right"
                    proposedPos.moveTo(Direction.RIGHT)
                    player.proposeMove(Direction.RIGHT, proposedPos)
            elif event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                    pass
    def start(self):
        pass

    def stop(self):
        pass
