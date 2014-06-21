import sys
import sdl2.ext
from graphicsManager import GraphicManager
from player import Player, Direction, Position


class InputManager(object):
    """processes the user input"""

    #TODO take away 0 to 4, passing it to -2 to 2 instead
    NUM_DIVISIONS_IN_AXIS = 5
    MOVE_MIDDLE_VALUE = 2 #int(round((self.NUM_DIVISIONS_IN_AXIS - 1) / 2))

    def __init__(self, graphicsManager):
        self.gMngr = graphicsManager 
        self.middlePoint = self.MOVE_MIDDLE_VALUE
        self.movePlayer = [self.middlePoint, self.middlePoint]

    def processUserInput(self, game):
        # TODO: issue. pass to generate events
        events = sdl2.ext.get_events()
        for event in events:
            #print event.type
            if event.type == sdl2.SDL_QUIT:
                print "QUIT"
                game.isRunning = False
            elif event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    self.movePlayer[1] = 0
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    self.movePlayer[1] = self.NUM_DIVISIONS_IN_AXIS - 1
                elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                    self.movePlayer[0] = 0
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    self.movePlayer[0] = self.NUM_DIVISIONS_IN_AXIS - 1
            elif event.type == sdl2.SDL_KEYUP:
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    self.movePlayer[1] = self.middlePoint
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    self.movePlayer[1] = self.middlePoint
                elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                    self.movePlayer[0] = self.middlePoint
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    self.movePlayer[0] = self.middlePoint
            elif event.type == sdl2.SDL_JOYAXISMOTION:
                # process the axis
                #print "Joystick ",
                #print [event.jaxis.axis, event.jaxis.which, event.jaxis.value]
                if event.jaxis.axis == 0:
                    #left joystick is axis 0 (h) & 1 (v);
                    self.movePlayer[0] = self.discreteValue(event.jaxis.value)
                elif event.jaxis.axis == 1:
                    self.movePlayer[1] = self.discreteValue(event.jaxis.value)
                elif event.jaxis.axis == 2:
                    #left trigger is axis 2;
                    pass
                elif event.jaxis.axis == 3:
                    #right joystick is axis 3 (h) & 4 (v);
                    pass
                elif event.jaxis.axis == 4:
                    pass
                elif event.jaxis.axis == 5:
                    #right trigger is axis 5
                    pass
            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                #print "joy DOWN...", 
                #print event.button. this doesn't work. it's a mousebutton object, not an id.
                pass
            elif event.type == sdl2.SDL_JOYBUTTONUP:
                #print "joy UP!"
                pass
            else:
                if event.type in (sdl2.SDL_WINDOW_INPUT_FOCUS, sdl2.SDL_WINDOW_INPUT_FOCUS):
                    # these are ignored
                    pass
                else: # 256, 1792, 1793, 1794 
                    # these are reported so we can decide wtf to do with them
                    print "UNKNOWN",
                    print event.type
        # generate overall events
        # move the player
        if self.movePlayer[0] != self.middlePoint or self.movePlayer[1] != self.middlePoint:
            player = game.ownPlayer
            proposedMove = (self.movePlayer[0], self.movePlayer[1])
            # TODO change to generate event
            player.proposedMove = proposedMove
        # orientate the player

    def discreteValue(self, originalValue):
        """returns a value from 0 to NUM_DIVISIONS_IN_AXIS not included"""
        return int(round(self.NUM_DIVISIONS_IN_AXIS * (originalValue + 32770) / 65540))

    def start(self):
        pass

    def stop(self):
        pass
