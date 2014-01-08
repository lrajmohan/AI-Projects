# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import copy

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def getStartState(self):
     """
     Returns the start state for the search problem
     """
     util.raiseNotDefined()

  def isGoalState(self, state):
     """
       state: Search state

     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  fringeList = util.Stack()
  print "fringeList",fringeList
  closedList = {str(problem.getStartState()): ([])} #Hash Map to maintain state to path
  print "closed list:", closedList
  isGoalStateArrived = False

  # Push start state into fringeList
  fringeList.push((problem.getStartState()))

  while not isGoalStateArrived and not fringeList.isEmpty():
        currentNode = fringeList.pop()
        print "currentNode",currentNode
        currentNodePath = closedList[str(currentNode)]
        print "currentNodepath:",currentNodePath
        # Explore children
        childrenOfCurrentNode = problem.getSuccessors(currentNode)
        print "childrenOfCurrentNode:",childrenOfCurrentNode
        for childNode in childrenOfCurrentNode:
            if str(childNode[0]) not in closedList:
                path = copy.copy(currentNodePath)
                path.append(childNode[1])
                print "child [0] %s, child [1] %s", childNode[0],childNode[1]
                print "path ", path
                fringeList.push(childNode[0])
                closedList[str(childNode[0])] = path # Put parent node in closed List
            if problem.isGoalState(childNode[0]):
                isGoalStateArrived = True
                goalState = childNode[0]
                break

        if isGoalStateArrived:
            #print closedList[str(problem.getStartState())]
            return closedList[str(goalState)]
  "util.raiseNotDefined()"

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"

  "*** YOUR CODE HERE ***"
  print "search.Start:", problem.getStartState()
  print "search.Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "search.Start's successors:", problem.getSuccessors(problem.getStartState())
  fringeList = util.Queue()
  closedList = {str(problem.getStartState()): ([])} #Hash Map to maintain state to path
  isGoalStateArrived = False

  # Push start state into fringeList
  fringeList.push((problem.getStartState()))

  while not isGoalStateArrived and not fringeList.isEmpty():
        currentNode = fringeList.pop()
        currentNodePath = closedList[str(currentNode)]
        # Explore children
        childrenOfCurrentNode = problem.getSuccessors(currentNode)
        print childrenOfCurrentNode
        for childNode in childrenOfCurrentNode:
            if str(childNode[0]) not in closedList:
                path = copy.copy(currentNodePath)
                path.append(childNode[1])
                fringeList.push(childNode[0])
                closedList[str(childNode[0])] = path # Put parent node in closed List
            if problem.isGoalState(childNode[0]):
                isGoalStateArrived = True
                goalState = childNode[0]
                break

        if isGoalStateArrived:
            #print closedList[str(problem.getStartState())]
            print "goal state",closedList[str(goalState)]
            return closedList[str(goalState)]


  """frontier = util.Queue()
  return greedySearch(problem, frontier, nullHeuristic)
  util.raiseNotDefined()"""
# Generates a solution from a solution node w/recursive parent pointers

"""def extractPath(solutionNode):
  path = []
  actions = []
  totalCost = 0
  upTravNode = solutionNode
  while upTravNode != None:
    path = [upTravNode[0][0]] + path		# include path
    actions = [upTravNode[0][1]] + actions	# include action
    upTravNode = upTravNode[1]			# look back 1 action in past
  return (path, actions, solutionNode[2])"""

def priorityfunction(item):
 return item[1]

def uniformCostSearch(problem):
 frontier = util.PriorityQueueWithFunction(priorityfunction)
 return greedySearch(problem, frontier, nullHeuristic)

"""Search the node of least total cost first.
  fringeList = util.PriorityQueue()
  closedList = {str(problem.getStartState()): ([])} #Hash Map to maintain state to path
  isGoalStateArrived = False

  # Push start state into fringeList
  fringeList.push((problem.getStartState()))

  while not isGoalStateArrived and not fringeList.isEmpty():
   currentNode = fringeList.pop()
   currentNodePath = closedList[str(currentNode)]
   # Explore children
   childrenOfCurrentNode = problem.getSuccessors(currentNode)
   for childNode in childrenOfCurrentNode:
    if str(childNode[0]) not in closedList:
     path = currentNodePath
     path.append(childNode[1])
     fringeList.push(childNode[0])
     closedList[str(childNode[0])] = path # Put parent node in closed List
    if problem.isGoalState(childNode[0]):
     isGoalStateArrived = True
     goalState = childNode[0]
    break
  if isGoalStateArrived:
   return closedList[str(goalState)]"""


"*** YOUR CODE HERE ***"
"""closed = []				# previously visited nodes
  fringe = util.PriorityQueue()		# unvisited []
  startState = problem.getStartState()
  counter = 0
  closed.append(startState)
  # if initialized in a goal state, return
  if problem.isGoalState(startState) == True:
    return ([], [], 0)
  # initializes the fringe with successors of the root
  pushToFringe = problem.getSuccessors(startState)
  for fringeNode in pushToFringe:
    tCost = fringeNode[2]
    fringe.push((fringeNode, None, tCost), tCost)
  # loop until a solution is found or no further possibilities exist
  while (fringe.isEmpty() == False):
    frngNode = fringe.pop()	# temp for breakdown into cur/parent nodes
    curtNode = frngNode[0]	# node for expansion, cost
    prntNode = frngNode[1]	# parent node [for path]
    cost = frngNode[2]		# cost up until this frngNode
    # if node is the goal, return solution information
    if problem.isGoalState(curtNode[0]):
      return (extractPath(frngNode))
    # else, check if the current node is in closed list
    if curtNode[0] not in closed:
      closed.append(curtNode[0])
      for fringeNode in problem.getSuccessors(curtNode[0]):
	tCost = cost+fringeNode[2]
        fringe.push((fringeNode, frngNode, tCost), tCost)"""
"util.raiseNotDefined()"

def greedySearch(problem, frontier, heuristic):
  import copy
  frontier.push((problem.getStartState(), 0))
  visitedstates = {str(problem.getStartState()) : (0, [])}
  endState = None
  endStateFound= False
  while not endStateFound and not frontier.isEmpty():
    currstate = frontier.pop()[0]
    currstatehistory = visitedstates[str(currstate)]
    currstatecost = currstatehistory[0]
    currstatepath = currstatehistory[1]
    newoptions = problem.getSuccessors(currstate)
    for option in newoptions:
      if str(option[0]) not in visitedstates:
        newpath = copy.copy(currstatepath)
        newpath.append(option[1])
        newstatehistory = (currstatecost+option[2]+heuristic(option[0], problem), newpath)
        visitedstates[str(option[0])] = newstatehistory
        frontier.push((option[0], currstatecost+option[2]))
        if problem.isGoalState(option[0]):
          endStateFound=True
          endState=option[0]
          break
  if endStateFound:
    return visitedstates[str(endState)][1]
  else:
    return []

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    fringeList = util.PriorityQueue()
    closedList = {str(problem.getStartState()): (0,[])} #Hash Map to maintain state to path & Value
    isGoalStateArrived = False

    # Push start state into fringeList
    fringeList.push((problem.getStartState()),0)

    while not isGoalStateArrived and not fringeList.isEmpty():
        currentNode = fringeList.pop()
        currentNodeData = closedList[str(currentNode)]
        currentNodeCost = currentNodeData[0]
        print heuristic(currentNode,problem)
        currentNodePath= currentNodeData[1]
        print "Current Node Cost",currentNodeCost
        # Explore children
        childrenOfCurrentNode = problem.getSuccessors(currentNode)
        #print childrenOfCurrentNode
       # print childrenOfCurrentNode
        for childNode in childrenOfCurrentNode:
            if str(childNode[0]) not in closedList:
                path = copy.copy(currentNodePath)
                path.append(childNode[1])
                closedList[str(childNode[0])] = (currentNodeCost+childNode[2],path) # Put parent node in closed List
                fringeList.push(childNode[0],currentNodeCost+childNode[2]+heuristic(childNode[0],problem))
            if problem.isGoalState(childNode[0]):
                isGoalStateArrived = True
                goalState = childNode[0]
                break

        if isGoalStateArrived:

            return closedList[str(goalState)][1]



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch