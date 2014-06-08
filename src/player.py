class Player(object):
    """represents a player of the game. not the user"""
    def __init__(self, direction, position):
        self.currentDir = direction
        self.currentPos = position
        self.porposedDir = None
        self.proposedPos = None

    def updatePosition(self, direction, position):
    	"""Updates position and direction erasing the proposed one if any"""
        self.currentDir = direction
        self.currentPos = position
        self.porposedDir = None
        self.proposedPos = None

    def updateStats(self, direction, position):
        # FUTURE to update the status of that player. getting tired etc.
        pass

    def proposeMove(self, direction, position):
    	"""Proposes a move for the player"""
        self.direction = direction
        self.position = position

class Direction(object):
    """represents the allowed move directions"""
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self, direction):
        if direction in (self.UP, self.DOWN, self.LEFT, self.RIGHT):
            self.direction = direction
        else:
            self.direction = None

class Position(object):
    """represents a position in the field"""
    STEP = 10

    def __init__(self, x, y):
    	self.x = x
    	self.y = y

    def set(self, x, y):
    	self.x = x
    	self.y = y

    def moveTo(self, direction):
		if direction == Direction.UP:
			self.y -= self.STEP
		elif direction == Direction.DOWN:
			self.y += self.STEP
		elif direction == Direction.LEFT:
			self.x -= self.STEP
		elif direction == Direction.RIGHT:
			self.x += self.STEP

