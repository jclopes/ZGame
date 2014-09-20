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

    def updateGame(self, game):
        # think if there is something to be done here. all should be onEvent instead?
         pass

    def onEvent(self, eclass, event):
        # TODO parse the Input and Server events and generate Final events
        if (eclass == EVENT_CLASS_INPUT):
            etype = event.etype
            if (etype == EventClassInput.TYPE_MOVE_DIRECTION):
                event.properties["player"].currentPos.applyMove(event.properties["proposedMove"])
            elif (etype == EventClassInput.TYPE_FACE_DIRECTION):
                event.properties["player"].currentDir = event.properties["proposedDir"]
        # TODO parse the server events in else statement
        pass

    def start(self):
        pass

    def stop(self):
        pass
