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

class Direction(object):
    """represents the allowed move directions"""

    def __init__(self, (x, y)):
        """x and y from -2 to +2"""

        self.direction_matrix = [[NW,  NNW,   N, NNE,   NE],
                                [NWW,  NW,    N, NE,    NEE],
                                [W,    W,     O, E,     E],
                                [SWW,  SW,    S, SE,    SEE],
                                [SW,   SSW,   S, SSE,   SE]]

        self.x = x + 2 # since the middle value is a 2 when doing a discrete
        self.y = y + 2
        self.direction = self.direction_matrix[y][x]

    def getDirection(self, x, y):
        return self.direction_matrix[x][y]
