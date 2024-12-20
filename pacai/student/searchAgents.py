"""
This file contains incomplete versions of some agents that can be selected to control Pacman.
You will complete their implementations.

Good luck and happy searching!
"""

import logging

from pacai.core import distance
from pacai.core.actions import Actions
from pacai.core.directions import Directions
from pacai.core.search.position import PositionSearchProblem
from pacai.core.search.problem import SearchProblem
from pacai.agents.base import BaseAgent
from pacai.agents.search.base import SearchAgent
from pacai.student.search import breadthFirstSearch

class CornersProblem(SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function.
    See the `pacai.core.search.position.PositionSearchProblem` class for an example of
    a working SearchProblem.

    Additional methods to implement:

    `pacai.core.search.problem.SearchProblem.startingState`:
    Returns the start state (in your search space,
    NOT a `pacai.core.gamestate.AbstractGameState`).

    `pacai.core.search.problem.SearchProblem.isGoal`:
    Returns whether this search state is a goal state of the problem.

    `pacai.core.search.problem.SearchProblem.successorStates`:
    Returns successor states, the actions they require, and a cost of 1.
    The following code snippet may prove useful:
    ```
        successors = []

        for action in Directions.CARDINAL:
            x, y = currentPosition
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if (not hitsWall):
                # Construct the successor.

        return successors
    ```
    """

    def __init__(self, startingGameState):
        super().__init__()

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top = self.walls.getHeight() - 2
        right = self.walls.getWidth() - 2

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                logging.warning('Warning: no food in corner ' + str(corner))

        # *** Your Code Here ***
        self.visited = []
        self.startState = (self.startingPosition, self.visited)
    
    def startingState(self):
        return self.startState
    
    def isGoal(self, state):
        coords = state[0]
        visited = state[1]
        self._visitedLocations.add(coords)
        self._visitHistory.append(coords)

        if coords not in self.corners:
            return False
        
        if len(visited) != len(self.corners):
            return False
        else:
            return True
    
    def successorStates(self, current):
        successors = []

        for action in Directions.CARDINAL:
            x, y = current[0]
            visited = current[1]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]

            if (not hitsWall):
                # Construct the successor.
                temp_visited = visited.copy()
                nextCoords = (nextx, nexty)
                if nextCoords in self.corners and nextCoords not in visited:
                    temp_visited.append(nextCoords)
                
                nextState = (nextCoords, temp_visited)
                successors.append((nextState, action, 1))
                
        # Bookkeeping for display purposes (the highlight in the GUI).
        self._numExpanded += 1
        if (current[0] not in self._visitedLocations):
            self._visitedLocations.add(current[0])
            # Note: visit history requires coordinates not states. In this situation
            # they are equivalent.
            coordinates = current[0]
            self._visitHistory.append(coordinates)

        return successors

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        This is implemented for you.
        """

        if (actions is None):
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999

        return len(actions)

def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem;
    i.e. it should be admissible.
    (You need not worry about consistency for this heuristic to receive full credit.)
    """

    # Useful information.
    # corners = problem.corners  # These are the corner coordinates
    # walls = problem.walls  # These are the walls of the maze, as a Grid.

    # *** Your Code Here ***
    # Return manhattan distance to the closest corner dot
    coords = state[0]
    visited = state[1]
    corners = problem.corners
    cornerList = []

    for corner in corners:
        if corner not in visited:
            cornerList.append((corner, distance.manhattan(coords, corner)))
    
    if len(cornerList) == 0:
        return 0
    elif len(cornerList) == 1:
        return cornerList[0][1]
    
    # Sort elements in cornerList from least to greatest based on manhattan distance
    for i in range(len(cornerList) - 1):
        for j in range(i, len(cornerList)):
            if cornerList[i][1] > cornerList[j][1]:
                temp = cornerList[i]
                cornerList[i] = cornerList[j]
                cornerList[j] = temp
    
    closest = cornerList[0][1]
    gap = distance.manhattan(cornerList[0][0], cornerList[1][0])
    if len(cornerList) == 2:
        return closest + gap
    
    gap2 = distance.manhattan(cornerList[1][0], cornerList[-1][0])
    return closest + gap + gap2

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.
    First, try to come up with an admissible heuristic;
    almost all admissible heuristics will be consistent as well.

    If using A* ever finds a solution that is worse than what uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!
    On the other hand, inadmissible or inconsistent heuristics may find optimal solutions,
    so be careful.

    The state is a tuple (pacmanPosition, foodGrid) where foodGrid is a
    `pacai.core.grid.Grid` of either True or False.
    You can call `foodGrid.asList()` to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, `problem.walls` gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use.
    For example, if you only want to count the walls once and store that value, try:
    ```
    problem.heuristicInfo['wallCount'] = problem.walls.count()
    ```
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount'].
    """

    position, foodGrid = state

    # *** Your Code Here ***
    foodList = foodGrid.asList()
    distList = []
    for food in foodList:
        distList.append((food, distance.maze(food, position, problem.startingGameState)))
    
    if len(distList) == 0:
        return 0
    
    elif len(distList) == 1:
        return distList[0][1]
    
    # Bubble Sort
    for i in range(len(distList) - 1):
        for j in range(i, len(distList)):
            if distList[i][1] > distList[j][1]:
                temp = distList[i]
                distList[i] = distList[j]
                distList[j] = temp

    farthest = distList[-1][0]
    next_farthest = distList[-2]

    gap1 = next_farthest[1]
    gap2 = distance.maze(next_farthest[0], farthest, problem.startingGameState)

    return gap1 + gap2
class ClosestDotSearchAgent(SearchAgent):
    """
    Search for all food using a sequence of searches.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, state):
        self._actions = []
        self._actionIndex = 0

        currentState = state

        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self._actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' %
                            (str(action), str(currentState)))

                currentState = currentState.generateSuccessor(0, action)

        logging.info('Path found with cost %d.' % len(self._actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState.
        """

        # Here are some useful elements of the startState
        # startPosition = gameState.getPacmanPosition()
        # food = gameState.getFood()
        # walls = gameState.getWalls()
        # problem = AnyFoodSearchProblem(gameState)

        # *** Your Code Here ***
        problem = AnyFoodSearchProblem(gameState)
        return breadthFirstSearch(problem)

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem,
    but has a different goal test, which you need to fill in below.
    The state space and successor function do not need to be changed.

    The class definition above, `AnyFoodSearchProblem(PositionSearchProblem)`,
    inherits the methods of `pacai.core.search.position.PositionSearchProblem`.

    You can use this search problem to help you fill in
    the `ClosestDotSearchAgent.findPathToClosestDot` method.

    Additional methods to implement:

    `pacai.core.search.position.PositionSearchProblem.isGoal`:
    The state is Pacman's position.
    Fill this in with a goal test that will complete the problem definition.
    """

    def __init__(self, gameState, start = None):
        super().__init__(gameState, goal = None, start = start)

        # Store the food for later reference.
        self.food = gameState.getFood().asList()
    
    def isGoal(self, state):
        if len(self.food) == 0 or state in self.food:
            return True
        return False


class ApproximateSearchAgent(BaseAgent):
    """
    Implement your contest entry here.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Get a `pacai.bin.pacman.PacmanGameState`
    and return a `pacai.core.directions.Directions`.

    `pacai.agents.base.BaseAgent.registerInitialState`:
    This method is called before any moves are made.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
