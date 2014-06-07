#! /usr/bin/env python

import sys
import sdl2.ext
from zgame import Game
from graphics import Graphics

# run in terminal: python sdl.py ../play_file.log 

def main():
 
    # create the graphics
    graphics = Graphics()
    graphics.drawTest()

    print "aaa"
    # cread file with input
    playFile = open(sys.argv[1], 'r')
    # create game and start it
    game = Game(playFile)
    game.run()

    # close graphics
    graphics.close()

if __name__ == '__main__':
    sys.exit(main())
