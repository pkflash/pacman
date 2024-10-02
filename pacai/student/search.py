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
    # Initialize current state, frontier stack, and reached set
    # TODO: Implement move stack
    current_state = problem.startingState()
    moves = Stack()
    frontier = Stack()
    reached = set()
    frontier.push(current_state)
    

    # While frontier is not empty:
    # 1. Pop frontier stack and set node to popped element
    # 2. Check if the node is the goal state: if it is, return it.
    # 3. If not, add the node to the set of explored nodes and push all unvisited successors onto the frontier stack
    while not frontier.isEmpty():
        current_state = frontier.pop()
        if problem.isGoal(current_state):
            return moves
        reached.add(current_state)
        successors = problem.successorStates(current_state)
        for state in successors:
            temp_node = state[0]
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
