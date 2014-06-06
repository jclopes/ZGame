import sys
import json
from world import World
from worldview import WorldView

class Game(object):

    def __init__(self, filedesc):
        self.world = World()
        self.worldView = WorldView(self.world)
        self.connection = filedesc

    def run(self):
        """Method that starts the game running."""
        counter = 10
        isRunning = True
        while isRunning:
            newState = self.readState()
            self.world.update(newState)
            self.worldView.draw()

            counter -= 1
            if counter <= 0:
                isRunning = False

    def readState(self):
        line = self.connection.readline().strip()
        return json.loads(line)
