import math
from direction import Direction

class Player(object):
    """represents a player of the game. not the user"""


    FACE_MOVE_RATIO = 0.5

    def __init__(self, moveDirection, position, faceDirection):
        self.moveDirection = moveDirection
        self.moveSpeed = 0
        self.position = position
        self.faceDirection = faceDirection

    def getNextPosition(self):
        """given the current data, calculates where the player would end up"""
        if (self.moveDirection.direction == Direction.O): #The player is not moving
            newPosX = self.position.x
            newPosY = self.position.y
        else: #the player is moving
            #calculate what would be the normal move for X and Y
            normalX = math.cos(self.moveDirection.getAngle()) * self.moveSpeed
            normalY = math.sin(self.moveDirection.getAngle()) * self.moveSpeed
            additionX = math.cos(self.faceDirection.getAngle()) * self.moveSpeed * self.FACE_MOVE_RATIO
            additionY = math.sin(self.faceDirection.getAngle()) * self.moveSpeed * self.FACE_MOVE_RATIO
            #calculate final position
            newPosX = self.position.x + int(math.floor(normalX + additionX))
            newPosY = self.position.y + int(math.floor(normalY + additionY))
        return Position(newPosX, newPosY) # TODO should return based on BOTH directions


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
