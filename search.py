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
        if V==objective[0]:#objective in the form of [(5,1)]
            explored.append(V)
            break    
        else:
            for i in set(maze.getNeighbors(V[0],V[1])):
                if maze.isValidMove(i[0],i[1])==True and i not in explored:#can lead to infinite loop
                    frontier.append(i)
                    parent[i]=V#key is son,value is parent
            explored.append(V)
    a=objective[0]
    path.append(a)
    while start not in path:
        path.appendleft(parent[a])
        a=parent[a]
    return list(path)

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
     #following pseudocode as much as I understood it on :https://www.geeksforgeeks.org/a-search-algorithm/ and http://coecsl.ece.illinois.edu/ge423/lecturenotes/AstarHandOut.pdf
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
            else:
                temp=temp
        for k in frontier:
            if fdist[k]==temp:
                V=k
                break
        frontier.remove(V)
        if V in explored:
            continue
        explored.append(V)
        #if the objective judgement is written in the loop of neighbor handlement, the states explored will increase around 100 in the bigMaze, found by trial-and-error
        if V==objective[0]:
            parent[V]=Last
            break
        for i in set(maze.getNeighbors(V[0],V[1])):#get Neighbors already contained isValidMove
            if i not in explored: # every i is a neighbor of V, a child of parent V
                temphdist=heuristic(i,objective[0])
                tempgdist=gdist[V]+heuristic(i,V)#current cost to i(successor)
                hdist[i]=temphdist
                gdist[i]=tempgdist
                if (i in frontier and fdist[i]<tempgdist+temphdist) :#explored doesn't need to be contained here since admissible heruistic mentioned by instructor in Piazza
                    continue
                else:
                    fdist[i]=hdist[i]+gdist[i]
                    parent[i]=V
                    frontier.append(i)
                    Last=V
            else: 
                continue
    a=objective[0]
    path.append(a)
    while start not in path:
        path.appendleft(parent[a])
        a=parent[a]
    return list(path)






                


def path_finder(start_point,objective_point,maze):
    path=deque()
    explored=deque()
    parent={}
    gdist={}
    hdist={}
    fdist={}
    def heruistic_corner(point1,point2):
        return max((point1[0]-point2[0]),abs(point1[1]-point2[1]))
    gdist[start_point]=0
    hdist[start_point]=heruistic_corner(start_point,objective_point)
    fdist[start_point]=gdist[start_point]+hdist[start_point]
    frontier=deque()
    frontier.append(start_point)
    while frontier:
        #print('frontier=',frontier)
        V=frontier.popleft()
        if V in explored:
            V=frontier.popleft()
        #    print('enter explored')
        if V==objective_point:#objective in the form of [(5,1)]
            explored.append(V)
            frontier=frontier
        #    print('BEFORE ELSE V=',V)
            break    
        else:
        #    print('V=',V)
            for i in maze.getNeighbors(V[0],V[1]):
                if maze.isValidMove(i[0],i[1])==True and i not in explored:#can lead to infinite loop
                    frontier.append(i)
                    parent[i]=V#key is son,value is parent
        #        print('frontier in i loop',frontier)
            explored.append(V)
        #    print('explored',explored)
    #print('finish while')
    a=objective_point
    path.append(a)
    while start_point not in path:
        path.appendleft(parent[a])
        a=parent[a]
    #print('list path=',path)
    return list(path)



def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    start=maze.getStart()
    objective=maze.getObjectives()
    fullpath=deque()
    i=1
    print('start=',start)
    print('objectives are',objective)
    while objective:
        path=path_finder(start,objective.pop(),maze)# IT IS IN LIST FORM
        #print('while loop path',path)
        if i==1:
            fullpath+=path
        else:
            fullpath+=path[1:]
        #print('fullpath',fullpath)
        start=fullpath[-1]
        i+=1
    print('fullpath=',fullpath)
    return list(fullpath)




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
