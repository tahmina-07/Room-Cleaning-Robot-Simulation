import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import numpy as np 


import math
import random

import ps2_visualize
import pylab


from ps2_verify_movement36 import testRobotMovement



class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)



class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        pos: a Position
        """
        #create a point 
        position = (int(pos.getX()), int(pos.getY))  
        #check if the point is in the isTileCleaned class if not added 
        if position is not self.isTileCleaned:
            self.isTileCleaned.append(position)