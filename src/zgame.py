import sys
import json
import time
from world import World
from worldview import WorldView
from graphicsmanager import GraphicManager
from player import Player, Position
from direction import Direction
from clock import Clock

class Game(object):

    S_UPDATE = 0.01
    S_TURN = 0.02


    def __init__(self, inputManager, updateManager, graphicsManager, soundManager, networkManager, filedesc):
        self.world = World()
        self.worldView = WorldView(self.world)
        self.iMngr = inputManager
        self.uMngr = updateManager
        self.gMngr = graphicsManager
        self.sMngr = soundManager
        self.nMngr = networkManager
        self.connection = filedesc
        self.isRunning = True
        self.ownPlayer = Player(Direction((2,0)), Position(50, 50),Direction((2,0)))

    def run(self):
        """Method that starts the game running."""

        timeController = Clock(self.S_TURN)

        self.isRunning = True
        while self.isRunning:
            # start turn
            timeController.start()
            leftTime = self.S_TURN

            #TODO think if input should be processed inside the inner loop
            # process user input to Game
            self.iMngr.processUserInput(self)
            #isRunning = not self.iMngr.closedGame()

            while timeController.time_left() > self.S_UPDATE:
                #sync with remote
                self.nMngr.updateGame(self)

                # update state of the game
                self.uMngr.updateGame(self)
                #newState = self.readState()
                #self.world.update(newState)

            # play sounds
            self.sMngr.updateGame(self)
            # render
            self.gMngr.draw(timeController.time_left(), self)
            #self.worldView.draw()

            # sleep if necessary
            timeController.sleep()

    def readState(self):
        line = self.connection.readline().strip()
        return json.loads(line)
