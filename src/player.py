class Player(object):
    """represents a player of the game. not the user"""

    # up is forward, down backwards. matrix represents amount of move
    move_matrix = [ [1,1,4,1,1],
                    [1,1,4,1,1],
                    [1,1,0,1,1],
                    [1,1,1,1,1],
                    [1,1,1,1,1]]
    NUM_DIVISIONS_IN_AXIS = 5
    MOVE_MIDDLE_VALUE = 2 #int(round((self.NUM_DIVISIONS_IN_AXIS - 1) / 2))

    def __init__(self, direction, position):
        self.currentDir = direction
        self.currentPos = position
        self.proposedDir = None
        self.proposedMove = (self.MOVE_MIDDLE_VALUE, self.MOVE_MIDDLE_VALUE)

    def updatePosition(self, direction, position):
        """Updates position and direction erasing the proposed one if any"""
        self.currentDir = direction
        self.currentPos = position
        self.proposedDir = None
        self.proposedPos = None
        self.proposedMove = (2,2)

    def updateStats(self, direction, position):
        # FUTURE to update the status of that player. getting tired etc.
        pass

    def proposeMove(self, direction, position):
        """Proposes a move for the player"""
        self.proposedDir = direction
        self.proposedPos = position

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
    #TODO the pixels that this moves should be in graphics
    STEP = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set(self, x, y):
        self.x = x
        self.y = y

    def applyMove(self, (movex, movey)):
        #TODO apply move matrix to enhance move
        # apply move
        self.x += movex - 2
        self.y += movey - 2

    def moveTo(self, direction):
        if direction == Direction.UP:
            self.y -= self.STEP
        elif direction == Direction.DOWN:
            self.y += self.STEP
        elif direction == Direction.LEFT:
            self.x -= self.STEP
        elif direction == Direction.RIGHT:
            self.x += self.STEP

