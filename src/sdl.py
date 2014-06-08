#! /usr/bin/env python

import sys
import sdl2.ext
from zgame import Game
from inputManager import InputManager
from graphicsManager import GraphicManager

# run in terminal: python sdl.py ../play_file.log 

def main():
 
    # create the managers
    gMngr = GraphicManager()
    iMngr = InputManager(gMngr)

    print "starting game"
    # create file with input
    playFile = open(sys.argv[1], 'r')
    # start the managers
    gMngr.start()
    iMngr.start()

    # create game and start it
    game = Game(iMngr, gMngr, playFile)
    game.run()

    # close the managers
    gMngr.stop()
    iMngr.stop()

if __name__ == '__main__':
    sys.exit(main())
