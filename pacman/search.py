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
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"

  frontier = util.Stack()
  frontier.push((problem.getStartState(), None, None))

  hasSeen = set()

  while not frontier.isEmpty():
    node = frontier.pop()
    state = node[0]
    for child, child_dir, _  in problem.getSuccessors(state):
      if child in hasSeen: continue
      if problem.isGoalState(child):
        path = unwrapPath((child, child_dir, node),1,2)
        return path
      hasSeen.add(child)
      frontier.push( (child, child_dir, node) )
  return None

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  frontier = util.Queue()
  frontier.push((problem.getStartState(), None, None))

  hasSeen = set()

  while not frontier.isEmpty():
    node = frontier.pop()
    state = node[0]
    for child, child_dir, _  in problem.getSuccessors(state):
      if child in hasSeen: continue
      if problem.isGoalState(child):
        return unwrapPath((child, child_dir, node),1,2)
      hasSeen.add(child)
      frontier.push( (child, child_dir, node) )
  return None
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  print('Starting UCS')
  frontier = util.PriorityQueue()
  frontier.push((0,problem.getStartState(), None, None),0)

  hasSeen = set()

  while not frontier.isEmpty():
    node = frontier.pop()
    cost = node[0]
    state = node[1]
    if problem.isGoalState(state):
      print 'Final cost',cost
      return unwrapPath(node,2,3)
    if state in hasSeen: continue
    hasSeen.add(state)
    print('Now serving',state)
    print('Successors will be',problem.getSuccessors(state))
    for child, child_dir, link_cost  in problem.getSuccessors(state):
      frontier.push( (cost + link_cost, child, child_dir, node), cost + link_cost )
  print 'Failed to find'
  return None

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  frontier = util.PriorityQueue()
  frontier.push((0,problem.getStartState(), None, None),0)

  hasSeen = set()

  while not frontier.isEmpty():
    node = frontier.pop()
    cost = node[0]
    state = node[1]
    if problem.isGoalState(state):
      print 'Final cost',cost
      return unwrapPath(node,2,3)
    if state in hasSeen: continue
    hasSeen.add(state)
    for child, child_dir, link_cost  in problem.getSuccessors(state):
      frontier.push( (cost + link_cost, child, child_dir, node), cost + link_cost + heuristic(child,problem) )
  return None
    

def unwrapPath(start, pluck_index, next_index):
  if start == None: return []
  path = []
  while start[pluck_index] != None:
    path.append(start[pluck_index])
    start = start[next_index]
  path.reverse()
  #print 'Final path'
  #print path
  return path

  
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
