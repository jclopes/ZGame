import sys
import sdl2.ext
from graphicsmanager import GraphicManager
from player import Player, Direction, Position
from eventmanager import EventPlayerMove, EventPlayerDirect
import pdb

class InputManager(object):
    """processes the user input"""

    #TODO take away 0 to 4, passing it to -2 to 2 instead
    NUM_DIVISIONS_IN_AXIS = 5
    MOVE_MIDDLE_VALUE = 2

    def __init__(self, eventManager, graphicsManager):
        self.eMngr = eventManager 
        self.gMngr = graphicsManager 
        self.middlePoint = self.MOVE_MIDDLE_VALUE
        self.movePlayer = [self.middlePoint, self.middlePoint]
        self.directPlayer = [2, 0] #East

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
                    self.directPlayer[0] = self.discreteValue(event.jaxis.value)
                elif event.jaxis.axis == 4:
                    self.directPlayer[1] = self.discreteValue(event.jaxis.value)
                elif event.jaxis.axis == 5:
                    #right trigger is axis 5
                    pass
            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                #id of button located in event.button.which
                #A 256, B 257, X 258, Y 259
                #LB 260 LR 261
                #joystick left click 262 right click 263
                #start 264, x 265, back 266
                #up 267 down 268 left 269 right 270
                print "joy DOWN...", 
                print event.button.which #this doesn't work. it's a mousebutton object, not an id.
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
            self.eMngr.addEvent(EventPlayerMove(player, proposedMove))
        # orientate the player
        if self.directPlayer[0] != 0 or self.directPlayer[1] != 0: # if there is a position
            player = game.ownPlayer
            proposedDir = Direction((self.directPlayer[0], self.directPlayer[1]))
            self.eMngr.addEvent(EventPlayerDirect(player, proposedDir))

    def discreteValue(self, originalValue):
        """returns a value from 0 to NUM_DIVISIONS_IN_AXIS not included"""
        return int(round(self.NUM_DIVISIONS_IN_AXIS * (originalValue + 32770) / 65540))

    def start(self):
        pass

    def stop(self):
        pass
