import sys
import json
from world import World
from worldview import WorldView
from graphicsManager import GraphicManager
from player import Player, Direction, Position

class Game(object):

    def __init__(self, inputManager, graphicsManager, filedesc):
        self.world = World()
        self.worldView = WorldView(self.world)
        self.iMngr = inputManager
        self.gMngr = graphicsManager
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

            # update state of the game
            #newState = self.readState()
            #self.world.update(newState)

            # render
            self.gMngr.drawTest2(self)
            #self.worldView.draw()

    def readState(self):
        line = self.connection.readline().strip()
        return json.loads(line)
