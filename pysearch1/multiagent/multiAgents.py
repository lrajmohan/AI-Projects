# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #Distance from nearest ghost
        dGhostmin = 'Inf'
        dGhostmax = 0
        for newGhostState in newGhostStates:
            gp=newGhostState.getPosition()
            md=manhattanDistance(newPos, newGhostState.getPosition())
            dGhostmin = min(dGhostmin, manhattanDistance(newPos, newGhostState.getPosition()))
            dGhostmax = max(dGhostmin, manhattanDistance(newPos, newGhostState.getPosition()))

        #Distance from nearest food
        dFoodmin = 'Inf'
        dFoodsum = 0
        newFoodList = newFood.asList()
        for newFoodPos in newFoodList:
            dFoodmin = min(dFoodmin, manhattanDistance(newPos, newFoodPos))
            dFoodsum = dFoodsum + manhattanDistance(newPos, newFoodPos)


        if dFoodmin == 0:
            scoreValue = 0
        else:
            # To give high score to move where food in near either minus the dFoodmin or add reciprocal of dFoodmin
            scoreValue = 1.0/(500.0*float(dFoodmin))
        # Discard all moves in which Distance from nearest ghost is less than 2 (give high negative value)
        # So pacman will not die
        if dGhostmin < 2:
            scoreValue = -100000

        return scoreValue + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):

  def minFunction(self, gameState, currentDepth, ghostIndex):
    #Terminal check - return the utility value of the current state
    if self.checkterminal(gameState, currentDepth):
        return self.evaluationFunction(gameState)



    #Retrieving the list of legal actions for the current ghost
    ghostLegalActions = gameState.getLegalActions(ghostIndex)

    #Looping thought the current ghost's moves
    for action in ghostLegalActions:
        newGameStates = [gameState.generateSuccessor(ghostIndex, action)]

    #Retrieving the number of ghosts from the game state
    nGhosts = gameState.getNumAgents() - 1
	
    #if the current ghost is the last ghost then call the max function
    # now else call the minimum function with the next ghost
    if(ghostIndex == nGhosts):
        for newGameState in newGameStates:
           ghostScores = [self.maxFunction(newGameState, currentDepth + 1)]
    # Looping Horizontally for all Ghosts and and their moves
    elif(ghostIndex < nGhosts):
        for newGameState in newGameStates:
           ghostScores = [self.minFunction(newGameState, currentDepth, ghostIndex + 1)]

    #returning the minimum value
    return min(ghostScores)

  def checkterminal(self,gameState,currentDepth):
      if self.depth == currentDepth:
          return True
      elif gameState.isLose():
          return True
      elif gameState.isWin():
          return True
      else:
          return False
  def maxFunction(self, gameState, currentDepth):
    #Terminal Check - it yes return the utility value of the game state
    if self.checkterminal(gameState, currentDepth):
        return self.evaluationFunction(gameState)

    #Generate the legal pacman actions
    pacmanLegalActions = gameState.getLegalPacmanActions()


    #For each of the valid pacman action, generate the successor moves
    for action in pacmanLegalActions:
        if not (action == 'STOP'):
            newGameStates = [gameState.generatePacmanSuccessor(action)]

    for newGameState in newGameStates:
        pacmanScores = [self.minFunction(newGameState, currentDepth , 1)]
    #Returning the maximum score
    return max(pacmanScores)

  def getAction(self, gameState):
      #Generating the legal moves
      legalMoves = gameState.getLegalPacmanActions()

      #Generating the successor game states from the current state
      newGameStates  = [gameState.generatePacmanSuccessor(action) for action in legalMoves]
      #Generating the scores of the successor game states - the recursion process starts by calling the minimum function
      scores = [self.minFunction(newGameState, 0,  1) for newGameState in newGameStates]
      #Retrieve the Maximum value from the child states
      bestScore = max(scores)
      #Retrieve teh index of the best node
      bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
      #If many are best, choose a random one
      chosenIndex = random.choice(bestIndices)
      #return the move corresponding to the best child game state
      return legalMoves[chosenIndex]

class AlphaBetaAgent(MultiAgentSearchAgent):

    def checkterminal(self,gameState,currentDepth):
        if self.depth == currentDepth:
            return True
        elif gameState.isLose():
            return True
        elif gameState.isWin():
            return True
        else:
            return False
    def minFunctionAB(self, gameState, currentDepth, ghostIndex, alpha, beta):
        #Terminal check - return the utility value of the current state
        if self.checkterminal(gameState, currentDepth):
            return self.evaluationFunction(gameState)

        #Retrieving the list of legal actions for the current ghost
        ghostLegalActions = gameState.getLegalActions(ghostIndex)
        betaLocal = float('Inf')
        #Looping thought the current ghost's moves
        for action in ghostLegalActions:
            newGameState = gameState.generateSuccessor(ghostIndex, action)
            #if the current ghost is the last ghost then call the max function
            # now else call the minimum function with the next ghost
            #Retrieving the number of ghosts from the game state
            nGhosts = gameState.getNumAgents() - 1
            if (ghostIndex < nGhosts):
            # Looping Horizontally for all Ghosts and and their moves
                #calculating the minimum value as score
                betaLocal = min(betaLocal, self.minFunctionAB(newGameState, currentDepth, ghostIndex + 1, alpha, beta))
            elif (ghostIndex == nGhosts):
                betaLocal = min(betaLocal, self.maxFunctionAB(newGameState, currentDepth + 1, alpha, beta))
            # updating beta as minimum of score value and beta
            beta = min(betaLocal, beta)
            #Alpha cut off
            if (alpha >= betaLocal):
                return betaLocal

        #returning the minimum value  as score
        return beta

    def maxFunctionAB(self, gameState, currentDepth, alpha, beta):
        #Terminal Check - it yes return the utility value of the game state
        if self.checkterminal(gameState, currentDepth):
            return self.evaluationFunction(gameState)

        #Generate the legal pacman actions
        pacmanLegalActions = gameState.getLegalPacmanActions()
        #Removing the Pacman's stop move
        pacmanLegalActions.remove(Directions.STOP)
        alphaLocal = float('-Inf')

        #For each of the valid pacman action, generate the successor moves
        for action in pacmanLegalActions:
            newGameState = gameState.generatePacmanSuccessor(action)
            #calculating the maximum  value as score
            alphaLocal = max(alphaLocal, self.minFunctionAB(newGameState, currentDepth, 1, alpha, beta))
            # updating alpha as maximum of score value and beta
            alpha = max(alpha, alphaLocal)
            # beta cut-off
            if (beta <= alphaLocal):
                return alphaLocal
        #Returning the maximum score
        return alpha

    def getAction(self, gameState):
        # alpha is best explored path for maxFunctionAB
        alpha = float('-Inf')
        # beta is best explored path for minFunctionAB
        beta = float('inf')
        # current score
        score = float('-Inf')
        #Generating the pacman legal moves
        pacmanLegalActions = gameState.getLegalPacmanActions()

        # Select the first move as best move
        bestAction = pacmanLegalActions[0]

        for action in pacmanLegalActions:
          if not (action == 'STOP'):
              #Generating the successor game states from the current state
              newGameState = gameState.generatePacmanSuccessor(action)
              #Generating the scores of the successor game states - the recursion process starts by calling the minimum function
              newScore = self.minFunctionAB(newGameState, 0, 1, alpha, beta)
          if(newScore > score):
            # update the maximum score and best action
            score = newScore
            bestAction = action
          if(beta <= newScore):
            return bestAction
          alpha = max(alpha, newScore)
        #return the move corresponding to the best child game state
        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()