
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import math
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    alpha_initial=arm.getArmAngle()[0]
    beta_initial=arm.getArmAngle()[1]
    alpha_limit=arm.getArmLimit()[0]#This function returns (min angle, max angle) of all arm links
    beta_limit=arm.getArmLimit()[1]
    rows = math.trunc((alpha_limit[1]-alpha_limit[0])/granularity + 1)
    columns = math.trunc((beta_limit[1]-beta_limit[0])/granularity + 1)
    maze_Map = [[WALL_CHAR for x in range(columns)] for y in range(rows)]
    alpha = alpha_limit[0] #minimum angle of alpha
    beta=beta_limit[0]
    offsets=[alpha_limit[0],beta_limit[0]]

    while alpha<=alpha_limit[1]:#doesn't exceed maximum of alpha
        beta=beta_limit[0]
        while beta<=beta_limit[1]:#doesn't exceed maximum of beta
            arm.setArmAngle((alpha,beta))
            armPosDist=arm.getArmPosDist()
            armPos=arm.getArmPos()
            armEnd=armPos[1][1]
            index=angleToIdx([alpha,beta], offsets, granularity)#assume offset=min, following rows/columns formula
            if (alpha==alpha_initial and beta==beta_initial) or (isValueInBetween([alpha,alpha+granularity], alpha_initial) and isValueInBetween([beta,beta+granularity], beta_initial)):# one direction for odd number case
                maze_Map[index[0]][index[1]]=START_CHAR
            
            elif doesArmTouchObjects(armPosDist,obstacles,isGoal=False):
                maze_Map[index[0]][index[1]]=WALL_CHAR
            elif isArmWithinWindow(armPos, window)==False:
                maze_Map[index[0]][index[1]]=WALL_CHAR
            #touching the goal but not with using arm tip
            elif doesArmTouchObjects(armPosDist,goals,isGoal=True) and doesArmTipTouchGoals(armEnd,goals)==False:
                maze_Map[index[0]][index[1]]=WALL_CHAR
            elif doesArmTipTouchGoals(armEnd,goals)==True :
                #need to modify the DOESARMTIPTOUCHGOALS function @11:47 2/13
                maze_Map[index[0]][index[1]]=OBJECTIVE_CHAR
            else:
                maze_Map[index[0]][index[1]]=SPACE_CHAR
            beta+=granularity
        alpha+=granularity
    return Maze(maze_Map, [alpha_limit[0], beta_limit[0]], granularity)