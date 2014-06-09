#! /usr/bin/env python

import sys
import sdl2.ext
from zgame import Game
from inputManager import InputManager
from graphicsManager import GraphicManager
from updateManager import UpdateManager

# run in terminal: python sdl.py ../play_file.log 

def main():
 
    # create the managers
    gMngr = GraphicManager()
    iMngr = InputManager(gMngr)
    uMngr = UpdateManager()

    print "starting game"
    # create file with input
    playFile = open(sys.argv[1], 'r')
    # start the managers
    gMngr.start()
    iMngr.start()
    uMngr.start()

    # create game and start it
    # FIXME playfile should be passed to the updateManager
    game = Game(iMngr, uMngr, gMngr, playFile)
    game.run()

    # close the managers
    uMngr.stop()
    iMngr.stop()
    gMngr.stop()

if __name__ == '__main__':
    sys.exit(main())
