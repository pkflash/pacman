"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""
from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue
from pacai.core.actions import Actions

class Node:

    # TODO: Implement path cost in Node class
    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.parent = parent
        self.action = action
    
    def __eq__(self, otherNode):
        return self.state == otherNode.state
    def __lt__(self, otherNode):
        return self.state < otherNode.state
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
    node = Node(problem.startingState())
    frontier = Stack()
    reached = set()
    frontier.push(node)
    

    # While frontier is not empty:
    # 1. Pop frontier stack and set node to popped element
    # 2. Check if the node is the goal state: if it is, return it.
    # 3. If not, add the node to the set of explored nodes and push all unvisited successors onto the frontier stack
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoal(node.state):
            moves = []  # Array to return
            parent = node.parent
            while parent is not None:
                moves.insert(0, node.action)
                node = parent
                parent = node.parent

            return moves

        reached.add(node.state)
        successors = problem.successorStates(node.state)
        print(successors)
        for state in successors:
            temp_state = state[0]
            temp_action = state[1]
            temp_node = Node(temp_state, temp_action, node)
            if temp_node not in frontier.list and temp_state not in reached:
                frontier.push(temp_node)
    return None



    
    


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    

    # *** Your Code Here ***
    # Initialize current state, frontier queue, and reached set
    node = Node(problem.startingState())
    frontier = Queue()
    reached = set()
    frontier.push(node)
    

    # While frontier is not empty:
    # 1. Pop frontier queue and set node to popped element
    # 2. Check if the node is the goal state: if it is, return it.
    # 3. If not, add the node to the set of explored nodes and push all unvisited successors onto the frontier queue
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoal(node.state):
            moves = []  # Array to return
            parent = node.parent
            while parent is not None:
                moves.insert(0, node.action)
                node = parent
                parent = node.parent

            return moves

        reached.add(node.state)
        successors = problem.successorStates(node.state)
        for state in successors:
            temp_state = state[0]
            temp_action = state[1]
            temp_node = Node(temp_state, temp_action, node)
            if temp_node not in frontier.list and temp_state not in reached:
                frontier.push(temp_node)
    return None

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    # Initialize current state, frontier queue, and reached set
    node = Node(problem.startingState())
    frontier = PriorityQueue()
    reached = set()




def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()
