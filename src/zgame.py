import sys
import json
from world import World
from worldview import WorldView
from graphicsManager import GraphicManager
from player import Player, Direction, Position

class Game(object):

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
        self.ownPlayer = Player(Direction(Direction.RIGHT), Position(50, 50))

    def run(self):
        """Method that starts the game running."""

        self.isRunning = True
        while self.isRunning:
            # process user input to Game
            self.iMngr.processUserInput(self)
            #isRunning = not self.iMngr.closedGame()

            #sync with remote
            self.nMngr.updateGame(self)

            # update state of the game
            self.uMngr.updateGame(self)
            #newState = self.readState()
            #self.world.update(newState)

            # play sounds
            self.nMngr.updateGame(self)
            # render
            self.gMngr.drawTest2(self)
            #self.worldView.draw()

    def readState(self):
        line = self.connection.readline().strip()
        return json.loads(line)
