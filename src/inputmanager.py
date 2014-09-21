import sys
import sdl2.ext
from graphicsmanager import GraphicManager
from player import Player, Position
from direction import Direction
from eventmanager import EventClassInput
import pdb
import math

class InputManager(object):
    """processes the user input"""

    #total divisions on each of the axis. the value passed is from -X to +X where X = half this total
    NUM_DIVISIONS_IN_AXIS = 5 #output range is -2 to 2
    MOVE_MIDDLE_VALUE = 0
    MAX_SPEED = 5 #output range for speed is 0 to 5
    MAX_JOYSTIK_VALUE = 32000

    def __init__(self, eventManager, graphicsManager):
        self.eMngr = eventManager 
        self.gMngr = graphicsManager 
        self.middlePoint = self.MOVE_MIDDLE_VALUE
        self.movePlayer = [self.middlePoint, self.middlePoint]
        self.directPlayer = [2, 0] #East

    def processUserInput(self, game):
        events = sdl2.ext.get_events()
        for event in events:
            #print event.type
            if event.type == sdl2.SDL_QUIT:
                self.eMngr.publishEvent(EventClassInput(EventClassInput.TYPE_EXIT, {}))
            elif event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_UP:
                    self.movePlayer[1] = -1 * self.MAX_JOYSTIK_VALUE
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    self.movePlayer[1] = self.MAX_JOYSTIK_VALUE
                elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                    self.movePlayer[0] = -1 * self.MAX_JOYSTIK_VALUE
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    self.movePlayer[0] = self.MAX_JOYSTIK_VALUE
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
                    self.movePlayer[0] = event.jaxis.value
                elif event.jaxis.axis == 1:
                    self.movePlayer[1] = event.jaxis.value
                elif event.jaxis.axis == 2:
                    #left trigger is axis 2;
                    pass
                elif event.jaxis.axis == 3:
                    #right joystick is axis 3 (h) & 4 (v);
                    self.directPlayer[0] = event.jaxis.value
                elif event.jaxis.axis == 4:
                    self.directPlayer[1] = event.jaxis.value
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
        # generate input events to communicate with the other managers
        # move the player passing a direction and a speed events
        if self.movePlayer[0] != self.middlePoint or self.movePlayer[1] != self.middlePoint:
            player = game.ownPlayer
            proposedSpeed = self.discreteSpeedValue(math.sqrt(self.movePlayer[0]**2+self.movePlayer[1]**2))
            self.eMngr.publishEvent(EventClassInput(EventClassInput.TYPE_SPEED, {"player": player, "speed": proposedSpeed}))
            proposedDir = Direction((self.discreteAxisValue(self.movePlayer[0]), self.discreteAxisValue(self.movePlayer[1])))
            self.eMngr.publishEvent(EventClassInput(EventClassInput.TYPE_MOVE_DIRECTION, {"player": player, "direction": proposedDir}))
        # orientate the player
        if self.directPlayer[0] != 0 or self.directPlayer[1] != 0: # if there is a position
            player = game.ownPlayer
            proposedDir = Direction((self.discreteAxisValue(self.directPlayer[0]), self.discreteAxisValue(self.directPlayer[1])))
            if(proposedDir.direction != Direction.O): # direction Origin does not get passed. Last non origin direction is left
                self.eMngr.publishEvent(EventClassInput(EventClassInput.TYPE_FACE_DIRECTION, {"player": player, "direction": proposedDir}))

    def discreteAxisValue(self, originalValue):
        """returns a value from -(NUM_DIVISIONS_IN_AXIS-1)/2 to (NUM_DIVISIONS_IN_AXIS-1)/2"""
        return (int(round(self.NUM_DIVISIONS_IN_AXIS * (originalValue + 32770) / 65540)))-(self.NUM_DIVISIONS_IN_AXIS-1)/2

    def discreteSpeedValue(self, originalValue):
        """returns a value from 0 to MAX_SPEED"""
        return (int(round(self.MAX_SPEED * originalValue / 37000)))

    def start(self):
        pass

    def stop(self):
        pass
