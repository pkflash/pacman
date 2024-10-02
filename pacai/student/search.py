"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""
from pacai.util.stack import Stack
from pacai.core.actions import Actions
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    # *** Your Code Here ***
    
    # Initialize node, frontier stack, and reached set
    node = problem.startingState()
    moves = []  # List of moves to return to agent
    if problem.isGoal(node):
        return moves
    frontier = Stack()
    moveset = Stack()
    frontier.push(node)
    reached = set()
    

    # While frontier is not empty:
    # 1. Pop frontier stack and set node to popped element
    # 2. Check if the node is the goal state: if it is, return it.
    # 3. If not, add the node to the set of explored nodes and push all unvisited successors onto the frontier stack
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoal(node):
            return moves
        reached.add(node)
        successors = problem.successorStates(node)
        for state in successors:
            temp_node = state[0]
            temp_move = state[1]
            if temp_node not in frontier.list and temp_node not in reached:
                frontier.push(temp_node)
    return None



    
    


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    raise NotImplementedError()

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()
