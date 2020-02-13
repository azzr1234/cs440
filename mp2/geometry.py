# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position (int,int):of the arm link, (x-coordinate, y-coordinate)
    """
    # angle is in degree form convert to radian form  
    angle=math.radians(angle)
    X_origin=start[0]
    Y_origin=start[1]
    delta_X=math.trunc(length*math.cos(angle))
    delta_Y=math.trunc(length*math.sin(angle))
    X_end=X_origin+delta_X
    Y_end=Y_origin-delta_Y
    return (X_end,Y_end)

def linecircleintersect(start_x,start_y,end_x,end_y,circle_x,circle_y,radius):#follow code in https://stackoverflow.com/questions/30844482/what-is-most-efficient-way-to-find-the-intersection-of-a-line-and-a-circle-in-py
    (x1, y1), (x2, y2) = (start_x - circle_x, start_y - circle_y), (end_x - circle_x, end_y - circle_y)
    dx,dy=(x2 - x1), (y2 - y1)
    dr = math.sqrt(dx**2+dy**2)
    determinant = x1 * y2 - x2 * y1
    discriminant=(radius**2)*(dr**2)-determinant**2
    if discriminant<0:
        return False
    else:
        intersections = [
            (circle_x + (determinant* dy + sign * (-1 if dy < 0 else 1) * dx * discriminant**.5) / dr ** 2,
             circle_y + (-determinant * dx + sign * abs(dy) * discriminant**.5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))] 
        vector_line=(end_x-start_x,end_y-start_y)
        intersection1=(intersections[0][0]-start_x,intersections[0][1]-start_y)
        intersection2=(intersections[1][0]-start_x,intersections[1][1]-start_y)
        if ((0<=intersection1[0]/vector_line[0]<=1) and (0<=intersection1[1]/vector_line[1]<=1)) or ((0<=intersection2[0]/vector_line[0]<=1) and (0<=intersection2[1]/vector_line[1]<=1)):
            return True
        else:
            return False
def doesArmTouchObjects(armPosDist, objects, isGoal=False):
    """Determine whether the given arm links touch any obstacle or goal

        Args:
            armPosDist (list): start and end position and padding distance of all arm links [(start, end, distance)]
            objects (list): x-, y- coordinate and radius of object (obstacles or goals) [(x, y, r)]
            isGoal (bool): True if the object is a goal and False if the object is an obstacle.
                           When the object is an obstacle, consider padding distance.
                           When the object is a goal, no need to consider padding distance.
        Return:
            True if touched. False if not.
    """
    result=[]
    for armPos in armPosDist: # armPoS IN ((100, 100), (135, 110), 4) FORM 
        start=armPos[0]
        start_x=start[0]
        start_y=start[1]
        end=armPos[1]
        end_x=end[0]
        end_y=end[1]
        pad_dist=armPos[2]
        for each_objects in objects:
            each_objects_x=objects[0][0]#i[0] IN FORM (120, 100, 5)
            each_objects_y=objects[0][1]
            each_objects_r=objects[0][2]
            distance1=math.sqrt((start_x-each_objects_x)**2+(start_y-each_objects_y)**2)
            distance2=math.sqrt((end_x-each_objects_x)**2+(end_y-each_objects_y)**2)
            if distance1<= each_objects_r or distance2<= each_objects_r:
                #line inside the object
                result.append(1)
            else:
        #check whether the line intersects the circle http://mathworld.wolfram.com/Circle-LineIntersection.html and code in https://stackoverflow.com/questions/30844482/what-is-most-efficient-way-to-find-the-intersection-of-a-line-and-a-circle-in-py
                if isGoal==True:
                    intersect=linecircleintersect(start_x,start_y,end_x,end_y,each_objects_x,each_objects_y,each_objects_r)#boolean
                    result.append(intersect)
                else:#not goal case need to consider padding distance
                    # not with padding distance contacts
                    intersect=linecircleintersect(start_x,start_y,end_x,end_y,each_objects_x,each_objects_y,each_objects_r)#boolean
                    if intersect==True:
                        result.append(1)
                    else:
                        intersect2=linecircleintersect(start_x,start_y,end_x,end_y,each_objects_x,each_objects_y,each_objects_r+pad_dist)#boolean
                        intersect3=linecircleintersect(start_x,start_y,end_x,end_y,each_objects_x,each_objects_y,each_objects_r-pad_dist)#boolean
                        if intersect2==True or intersect3==True:
                            result.append(1)
                        else:
                            result.append(0)
    if sum(result)>0:
        return True
    else:
        return False

def doesArmTipTouchGoals(armEnd, goals):
    """Determine whether the given arm tip touch goals

        Args:
            armEnd (tuple): the arm tip position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]. There can be more than one goal.
        Return:
            True if arm tick touches any goal. False if not.
    """
    result=[]
    for goal in goals:
        dx=armEnd[0]-goal[0]
        dy=armEnd[1]-goal[1]
        r=goal[2]
        distance=math.sqrt((dx)**2+(dy)**2)
        if distance>r:
            return False
    return True


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end positions of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False if not.
    """
    width=window[0]
    height=window[1]
    for arm in armPos:#arm ((x,y),(x,y))
        arm_x1=arm[0][0]
        arm_y1=arm[0][1]
        arm_x2=arm[1][0]
        arm_y2=arm[1][1]
        if arm_x1>width or arm_x1<0 or arm_y1>height or arm_y1<0 or arm_x2>width or arm_x2<0 or arm_y2>height or arm_y2<0:
            return False  
    return True


if __name__ == '__main__':
    computeCoordinateParameters = [((150, 190),100,20), ((150, 190),100,40), ((150, 190),100,60), ((150, 190),100,160)]
    resultComputeCoordinate = [(243, 156), (226, 126), (200, 104), (57, 156)]
    testResults = [computeCoordinate(start, length, angle) for start, length, angle in computeCoordinateParameters]
    assert testResults == resultComputeCoordinate
    testArmPosDists = [((100,100), (135, 110), 4), ((135, 110), (150, 150), 5)]
    testObstacles = [[(120, 100, 5)], [(110, 110, 20)], [(160, 160, 5)], [(130, 105, 10)]]
    resultDoesArmTouchObjects = [
        True, True, False, True, False, True, False, True,
        False, True, False, True, False, False, False, True
    ]

    testResults = []
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle))
         #   print('isGoalNottrue',testArmPosDist,'obstacled tested',testObstacle)
         #   print(doesArmTouchObjects([testArmPosDist], testObstacle))

    #print("\n")
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))
         #   print('isGoal=true case',testArmPosDist,'obstacled tested',testObstacle)
         #   print(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))
    print('testResults= line159',testResults)

    assert resultDoesArmTouchObjects == testResults

    testArmEnds = [(100, 100), (95, 95), (90, 90)]
    testGoal = [(100, 100, 10)]
    resultDoesArmTouchGoals = [True, True, False]

    testResults = [doesArmTipTouchGoals(testArmEnd, testGoal) for testArmEnd in testArmEnds]
    assert resultDoesArmTouchGoals == testResults

    testArmPoss = [((100,100), (135, 110)), ((135, 110), (150, 150))]
    testWindows = [(160, 130), (130, 170), (200, 200)]
    resultIsArmWithinWindow = [True, False, True, False, False, True]
    testResults = []
    for testArmPos in testArmPoss:
        for testWindow in testWindows:
            testResults.append(isArmWithinWindow([testArmPos], testWindow))
    #print('testResults= line193',testResults)
    assert resultIsArmWithinWindow == testResults

    print("Test passed\n")
