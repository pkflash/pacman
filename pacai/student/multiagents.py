import random
from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core import distance


class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        newPosition = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()

        # Compute distance to closest food
        distances = [(food, distance.maze(newPosition, food, currentGameState)) for food in oldFood]
        distances.sort(key = lambda x: x[1])
        min_distance = distances[0][1]


        # Compute minimum ghost distance and check if pac man is about to die
        closest_ghost = 0
        closest_ghost_obj = None
        if len(newGhostStates) != 0:
            # Initialize closest_ghost with first element in newGhostStates
            closest_ghost = distance.manhattan(newPosition, newGhostStates[0].getPosition())

        for ghost in newGhostStates:
            pos = ghost.getPosition()  # Sometimes pos contains floats
            temp_dist = distance.manhattan(newPosition, pos)
            if temp_dist < 2 and ghost.getScaredTimer() != 0:
                return 1000
            elif temp_dist < 2:
                return -1000
            elif temp_dist < closest_ghost:
                closest_ghost = temp_dist

        
        return successorGameState.getScore() - min_distance * 2 + closest_ghost

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
    
    def min_value(self, state, agent, depth):
        if depth == self.getTreeDepth() or state.isOver():
            return self.getEvaluationFunction()(state)
        value = float('inf')
        actions = state.getLegalActions(agent)
        # Call max_value function if this is the last ghost
        # Increment depth only after all ghosts are explored
        if agent == state.getNumAgents() - 1:
            for action in actions:
                next_state = state.generateSuccessor(agent, action)
                value = min(value, self.max_value(next_state, 0, depth + 1))
            return value
        
        else:
            for action in actions:
                next_state = state.generateSuccessor(agent, action)
                value = min(value, self.min_value(next_state, agent + 1, depth))
            return value
    
    def max_value(self, state, agent, depth):
        if depth == self.getTreeDepth() or state.isOver():
            return self.getEvaluationFunction()(state)
        value = float('-inf')

        # This function only gets called for pac-man
        actions = state.getLegalActions(agent)
        for action in actions:
            next_state = state.generateSuccessor(agent, action)
            value = max(value, self.min_value(next_state, agent + 1, depth))
        return value



    def getAction(self, gameState):
        moves = []
        actions = gameState.getLegalActions()
        actions.remove("Stop")
        
        # Generate successor state
        # Get agent that last moved in successor state
        # Generate min value of state and agent
        # Append (action, value) pair to moves
        for action in actions:
            next_state = gameState.generateSuccessor(0, action)
            agent = next_state.getLastAgentMoved()
            pair = (action, self.min_value(next_state, agent + 1, 0))
            moves.append(pair)
        
        # Get max value of all pairs
        final_action = max(moves, key=lambda pair: pair[1])
        return final_action[0]




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    return currentGameState.getScore()

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
