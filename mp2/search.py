# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush

def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None. 
    """
    start=maze.getStart()
    objective=maze.getObjectives()
    path=deque()
    explored=deque()
    frontier=deque()
    frontier.append(start)
    parent={}
    while frontier:
        V=frontier.pop()
        if V==objective[0]:#objective in the form of [(5,1)]
            explored.append(V)
            break    
        else:
            for i in set(maze.getNeighbors(V[0],V[1])):
                if maze.isValidMove(i[0],i[1])==True and i not in explored :#can lead to infinite loop#and i not in explored
                    frontier.append(i)
                    parent[i]=V#key is son,value is parent
            explored.append(V)
    a=objective[0]
    path.append(a)
    while start not in path:
        path.appendleft(parent[a])
        a=parent[a]
    return []
#    list(path)