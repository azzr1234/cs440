# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)
from collections import deque
import sys
import maze

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)

# bfs passed test 1/31 19:04
def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start=maze.getStart()
    objective=maze.getObjectives()
    path=deque()
    explored=deque()
    frontier=deque()
    frontier.append(start)
    parent={}
    while frontier:
        V=frontier.popleft()
        if V in explored:
            V=frontier.popleft()
    #    print('V=',V)
    #    print('explored=',explored)
        if V==objective[0]:#objective in the form of [(5,1)]
            explored.append(V)
            break    
        else:
            for i in set(maze.getNeighbors(V[0],V[1])):
                if maze.isValidMove(i[0],i[1])==True and i not in explored:#can lead to infinite loop
                    frontier.append(i)
                    parent[i]=V#键是子，值是母
    #        print('Frontier=',frontier)
            explored.append(V)
    #print('parent=',parent)
    a=objective[0]
    path.append(a)
    while start not in path:
        path.appendleft(parent[a])
        a=parent[a]
    #print('Path=',path)
    #print('Validity', maze.isValidPath(path))
    return list(path)
    #return []


def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    start=maze.getStart()
    objective=maze.getObjectives()
    path=deque()
    explored=deque()
    frontier=deque()
    parent={}
    gdist={}
    hdist={}
    fdist={}
    frontier.append(start)
    gdist[start]=0
    def heuristic(point1,point2):
        return abs(point1[0]-point2[0])+abs(point1[1]-point2[1])
    hdist[start]=heuristic(start,objective[0])
    fdist[start]=gdist[start]+hdist[start]
    while frontier:
        temp=100000
        for i in frontier:
            if fdist[i]<temp:
                temp=fdist[i] #getting minmium fdict value in frontier elements
        for k in frontier:
            if fdist[k]==temp:
                V=k
       # print('V=',V)
       # print('frontier=',frontier)
        frontier.remove(V)
        for i in maze.getNeighbors(V[0],V[1]):
            if maze.isValidMove(i[0],i[1])==True: 
                if i==objective[0]:
                    hdist[i]=heuristic(i,objective[0])
                    gdist[i]=gdist[V]+1
                    parent[i]=V
                    break
                else:
                    temphdist=heuristic(i,V)
                    tempgdist=gdist[V]+1
                   # every i is V's neighbor
                    if (i in frontier and fdist[i]<temphdist+tempgdist) or(i in explored and fdist[i]<tempgdist+temphdist):# 13:24 state number wrong change one frontier condition to below
                        continue
                    else:
                        hdist[i]=heuristic(i,V)
                        gdist[i]=gdist[V]+1
                        fdist[i]=hdist[i]+gdist[i]
                        parent[i]=V
                        frontier.append(i)
        explored.append(V)
        #following pseudocode as much as I understood it on :https://www.geeksforgeeks.org/a-search-algorithm/
    a=objective[0]
    path.append(a)
    while start not in path:
        path.appendleft(parent[a])
        a=parent[a]
   # print('Path=',path)
   # print('Validity', maze.isValidPath(path))
    return list(path)
    #return []

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    return []

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []


def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
