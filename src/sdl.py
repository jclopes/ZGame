#! /usr/bin/env python

import sys
import sdl2.ext
from zgame import Game
from event_manager import EventManager
from inputManager import InputManager
from graphicsManager import GraphicManager
from updateManager import UpdateManager
from soundManager import SoundManager
from networkManager import NetworkManager

# run in terminal: python sdl.py ../play_file.log 

def main():
 
    # create the managers
    eMngr = EventManager()
    gMngr = GraphicManager(eMngr)
    iMngr = InputManager(eMngr, gMngr)
    uMngr = UpdateManager(eMngr)
    sMngr = SoundManager(eMngr)
    nMngr = NetworkManager(eMngr)

    print "starting game"
    # create file with input
    playFile = open(sys.argv[1], 'r')
    # start the managers
    eMngr.start()
    gMngr.start()
    iMngr.start()
    uMngr.start()
    sMngr.start()
    nMngr.start()

    # create game and start it
    # FIXME playfile should be passed to the updateManager
    game = Game(iMngr, uMngr, gMngr, sMngr, nMngr, playFile)
    game.run()

    # close the managers
    eMngr.stop()
    uMngr.stop()
    iMngr.stop()
    gMngr.stop()
    sMngr.stop()
    nMngr.stop()

if __name__ == '__main__':
    sys.exit(main())
