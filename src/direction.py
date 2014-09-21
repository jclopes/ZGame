import math

class Direction(object):
    """represents the allowed move directions"""

    NWW = 0
    NW = 1
    NNW = 2
    N = 3
    NNE = 4
    NE = 5
    NEE = 6
    E = 7
    SEE = 8
    SE = 9
    SSE = 10
    S = 11
    SSW = 12
    SW = 13
    SWW = 14
    W = 15
    O = 16

    direction_matrix = [[NW,  NNW,   N, NNE,   NE],
                        [NWW,  NW,    N, NE,    NEE],
                        [W,    W,     O, E,     E],
                        [SWW,  SW,    S, SE,    SEE],
                        [SW,   SSW,   S, SSE,   SE]]

    nameToAngle = { NWW: -153,
    NW:-135,
    NNW:-117,
    N:-90,
    NNE:-63,
    NE:-45,
    NEE:-27,
    E:0,
    SEE:27,
    SE:45,
    SSE:63,
    S:90,
    SSW:117,
    SW:135,
    SWW:153,
    W:180,
    O:0 }


    def __init__(self, (x, y)):
        """x and y from -2 to +2"""
        shiftPositions = 2 # we add 2 to shift the scale to 0 to 4
        self.direction = self.direction_matrix[y+shiftPositions][x+shiftPositions]

        #not used. instead we use the matrix
        # self.angle = math.atan2(y,x)/math.pi*180
        # print self.direction, self.angle

    def getDirection(self, x, y):
        return self.direction_matrix[x][y]

    def getAngle(self):
        """return the angle in radiants of the current direction"""
        return math.radians(self.nameToAngle[self.direction])

