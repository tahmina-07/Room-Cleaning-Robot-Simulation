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
        if position not in self.cleaned_tiles:
            self.cleaned_tiles.append(position)

      def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        self.m = m
        self.n = n

        
        point = (self.m, self.n)
        if point in  self.cleaned_tiles:
            return True 
        else:
            return False 
    
      def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.height * self.width
    
      def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleaned_tiles)
     def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        r_x = random.uniform(0, self.width)
        r_y = random.uniform(0, self.height)
        
        return Position(r_x, r_y)
     def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if pos.x >= 0 and pos.x < self.width and pos.y >= 0 and pos.y < self.height:
            return True
        else:
            return False 

class Robot(object):
    """
    Represents a robot cleaning a particular room.
    """
    def __init__(self, room, speed):
        """
        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room 
        self.speed = speed 
        self.position = room.getRandomPosition()
        self.direction = random.randint(0, 359)
    
    
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction
    
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position
    
     def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction 

class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        next_position = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        if self.room.isPositionInRoom(next_position) == False:
           self.setRobotDirection(random.randint(0, 359))
        else:
           self.setRobotPosition(next_position)            
           self.room.cleanTileAtPosition(next_position)

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    results = []
    for i in range(num_trials):
       #anim = ps2_visualize.RobotVisualization(num_robots, width, height)
       num_steps = 0
       # Instantiate a new room
       room = RectangularRoom(width, height)
       # Instantiate the robots
       robots = [robot_type(room, speed) for j in range(num_robots)]
       while (room.getNumCleanedTiles()/room.getNumTiles()) < min_coverage:
           num_steps += 1
           #anim.update(room, robots)
           for k in robots:
               k.updatePositionAndClean()
           if (room.getNumCleanedTiles()/room.getNumTiles()) >= min_coverage:
               results.append(num_steps)
               #anim.done()
           else:
               continue
    return sum(results)/len(results)
   
      

