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






                



def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.
    @param maze: The maze to execute the search on.
    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    # TODO: Write your code here
    start_point=maze.getStart()
    objective_lists=maze.getObjectives()#objective is a list
    fullpath=deque()
    counter=1
    print('start=',start_point)
    print('objectives are',objective_lists)
    def heuristic_objectives(start,objectivelist):#return an objective following the heuristic out of the whole list
        temp=list()
        for i in objectivelist:
            temp.append(abs(start[0]-i[0])+abs(start[1]-i[1]))
        threshold=min(temp)
        return threshold
    while objective_lists:# objectlist is not empty
        path=deque()
        explored=deque()
        parent={}
        gdist={}
        hdist={}
        fdist={}
        gdist[start_point]=0
        hdist[start_point]=heuristic_objectives(start_point,objective_lists)
        fdist[start_point]=gdist[start_point]+hdist[start_point]
        frontier=deque()
        frontier.append(start_point)
        # for a single path 
        while frontier:
            V=frontier.popleft()
            if V in explored:
                V=frontier.popleft()
            if V in objective_lists:#objective in the form of [(5,1)]
                explored.append(V)
                objective_lists.remove(V)
                #last element in explored is the objective in this path
                break    
            else:
                for i in maze.getNeighbors(V[0],V[1]):
                    if maze.isValidMove(i[0],i[1])==True and i not in explored:#can lead to infinite loop
                        temphdist=heuristic_objectives(i,objective_lists)
                        tempgdist=gdist[V]+1#current cost to i(successor)
                        if i in frontier and fdist[i]<tempgdist+temphdist:
                            continue
                        else:
                            fdist[i]=temphdist+tempgdist
                            hdist[i]=temphdist
                            gdist[i]=tempgdist
                            frontier.append(i)
                            parent[i]=V#key is son,value is parent
                            Last=V
                explored.append(V)
        #print('start point=',start_point)
        a=explored[-1]
        path.appendleft(a)
        while start_point not in path:
            a=parent[a]
            path.appendleft(a)
        #print('a=',a)
        #print('path=',path)
        start_point=explored[-1]
        if counter==1:
            fullpath+=path
        else:
            path.remove(a)
       #     print('path to +',path)
            fullpath+=path
        counter+=1
       # print('counter=',counter)
       # print('fullpath',fullpath)
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