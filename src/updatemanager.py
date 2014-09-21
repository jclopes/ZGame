import sys
from player import Player, Position
from direction import Direction
from eventmanager import EventManager, EVENT_CLASS_INPUT, EVENT_CLASS_SERVER, EventSubscriber, EventClassInput

class UpdateManager(EventSubscriber):
    """updates the game"""
    def __init__(self, eventManager):
        self.eMngr = eventManager 
        eventManager.subscribe(EVENT_CLASS_INPUT, self)
        eventManager.subscribe(EVENT_CLASS_SERVER, self)
        self.inputEvents = list()
        self.serverEvents = list()

    def updateGame(self, game):
        # TODO generate Final events (if the model is not used to pass that information)
        numEvents = len(self.inputEvents)
        while numEvents > 0:
            event = self.inputEvents.pop(0) #get the first element
            etype = event.etype
            if (etype == EventClassInput.TYPE_SPEED):
                event.properties["player"].moveSpeed = event.properties["speed"]
            elif (etype == EventClassInput.TYPE_MOVE_DIRECTION):
                player = event.properties["player"]
                player.moveDirection = event.properties["direction"]
                #TODO the new position should be checked against objects (collision detection) etc instead of being directly applied
                player.position = player.getNextPosition()
            elif (etype == EventClassInput.TYPE_FACE_DIRECTION):
                event.properties["player"].faceDirection = event.properties["direction"]
            elif (etype == EventClassInput.TYPE_EXIT):
                game.isRunning = False
            numEvents -= 1

        numEvents = len(self.serverEvents)
        while numEvents > 0:
            event = self.serverEvents.pop(0) #get the first element
            etype = event.etype
            #TODO process Server events
            numEvents -= 1
            pass

    def onEvent(self, eclass, event):
        # TODO store Input events instead of processing them
        if (eclass == EVENT_CLASS_INPUT):
            self.inputEvents.append(event)
        elif (eclass == EVENT_CLASS_SERVER):
            self.serverEvents.append(event)

    def start(self):
        pass

    def stop(self):
        pass
