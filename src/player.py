
NUM_DIVISIONS_IN_AXIS = 5
MOVE_MIDDLE_VALUE = 2


class Player(object):
    """represents a player of the game. not the user"""

    # up is forward, down backwards. matrix represents amount of move
    move_matrix = [ [1,1,4,1,1],
                    [1,1,4,1,1],
                    [1,1,0,1,1],
                    [1,1,1,1,1],
                    [1,1,1,1,1]]

    def __init__(self, direction, position):
        self.currentDir = direction
        self.currentPos = position

    def updatePosition(self, direction, position):
        """Updates position and direction erasing the proposed one if any"""
        self.currentDir = direction
        self.currentPos = position

    def updateStats(self, direction, position):
        # FUTURE to update the status of that player. getting tired etc.
        pass

    def proposeMove(self, direction, position):
        """Proposes a move for the player"""
        self.proposedDir = direction
        self.proposedPos = position


class Direction(object):
    """represents the allowed move directions"""

    def __init__(self, (x, y)):
        """x and y from -2 to +2"""
        self.NWW = 0
        self.NW = 1
        self.NNW = 2
        self.N = 3
        self.NNE = 4
        self.NE = 5
        self.NEE = 6
        self.E = 7
        self.SEE = 8
        self.SE = 9
        self.SSE = 10
        self.S = 11
        self.SSW = 12
        self.SW = 13
        self.SWW = 14
        self.W = 15

        self.O = 16

        self.direction_matrix = [[self.NW,  self.NNW,   self.N, self.NNE,   self.NE],
                                [self.NWW,  self.NW,    self.N, self.NE,    self.NEE],
                                [self.W,    self.W,     self.O, self.E,     self.E],
                                [self.SWW,  self.SW,    self.S, self.SE,    self.SEE],
                                [self.SW,   self.SSW,   self.S, self.SSE,   self.SE]]

        self.x = x + MOVE_MIDDLE_VALUE
        self.y = y + MOVE_MIDDLE_VALUE
        self.direction = self.direction_matrix[x][y]

    def getDirection(self, x, y):
        return self.direction_matrix[x][y]


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

