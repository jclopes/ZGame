import sys
import sdl2.ext
from graphicsManager import GraphicManager
from player import Player, Direction, Position

class InputManager(object):
    """processes the user input"""
    def __init__(self, graphicsManager):
        self.gMngr = graphicsManager

    def processUserInput(self, game):
        # FIXME: we are automatically updating the position object and we should be creating a new one instead.
        # TODO: issue. this function can just be used for Game and should be available for other parts as a menu?
        events = sdl2.ext.get_events()
        for event in events:
#            print event.type
            if event.type == sdl2.SDL_QUIT:
                print "QUIT"
                game.isRunning = False
            if event.type == sdl2.SDL_KEYDOWN:
                player = game.ownPlayer
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    print "up"
                    player.proposeMove(Direction.UP, player.currentPos.moveTo(Direction.UP))
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    print "down"
                    player.proposeMove(Direction.DOWN, player.currentPos.moveTo(Direction.DOWN))
                elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                    print "left"
                    player.proposeMove(Direction.LEFT, player.currentPos.moveTo(Direction.LEFT))
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    print "right"
                    player.proposeMove(Direction.RIGHT, player.currentPos.moveTo(Direction.RIGHT))
            elif event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym in (sdl2.SDLK_UP, sdl2.SDLK_DOWN):
                    pass
    def start(self):
        pass

    def stop(self):
        pass
