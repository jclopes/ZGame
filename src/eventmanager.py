import sys
from player import Player

# list all vent types
EVENT_TYPE_PLAYER_MOVE = 0
EVENT_TYPE_PLAYER_REDIRECT = 1
EVENT_TYPE_GAME_CLOSE = 2

EVENT_TYPES = [EVENT_TYPE_PLAYER_MOVE, EVENT_TYPE_PLAYER_REDIRECT, EVENT_TYPE_GAME_CLOSE]


class EventManager(object):
    """handles the events between managers in the game"""

    def __init__(self):
        # initialize the right queues for each type
        # loops the event types creating a list for each of those
        self.subscriberQueues = dict()
        for eventType in EVENT_TYPES:
            self.subscriberQueues[eventType] = list()

    # publishes an event of eType. eType must have been defined. returns success on ok publishing
    def publishEvent(self, event):
        # TODO check for the right queue. contact all subscribers.
        for subscriber in self.subscriberQueues[event.type]:
            subscriber.onEvent(event.type, event)

    # adds a new class to the subscriber to that eType. return success on ok subscription
    def subscribe(self, etype, subscriber):
        # TODO check for the right queue. add subscriber to queue
        self.subscriberQueues[etype].append(subscriber)

    # deletes the new class from the queue. return success on ok subscription
    def unsubscribe(self, etype, subscriber):
        # TODO check for the right queue. delete subscriber to queue
        self.subscriberQueues[etype].remove(subscriber)

    def start(self):
        pass

    def stop(self):
        pass


class EventSubscriber(object):
    """represents a subscriber of events"""

    def onEvent(self, etype, event):
        raise NotImplemented


class Event(object):
    """represents an event in the game"""

    def __init__(self, etype):
        self.type = etype


class EventPlayerMove(Event):
    """represents an event for a player moving"""

    def __init__(self, player, move):
        super(EventPlayerMove, self).__init__(EVENT_TYPE_PLAYER_MOVE)
        self.player = player
        self.move = move

class EventPlayerDirect(Event):
    """represents an event for a player changeing position"""

    def __init__(self, player, direction):
        super(EventPlayerDirect, self).__init__(EVENT_TYPE_PLAYER_REDIRECT)
        self.player = player
        self.direction = direction

