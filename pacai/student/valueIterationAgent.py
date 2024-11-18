from pacai.agents.learning.value import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dictionary which holds the q-values for each state.

        # Compute the values here.
        states = self.mdp.getStates()
        for state in states:
            self.values[state] = self.getValue(state)
        
        for i in range(self.iters):
            temp_values = dict(self.values)
            for state in states:
                # Get max q value out of all actions in mdp.getPossibleActions
                q_value = float('-inf')
                for action in self.mdp.getPossibleActions(state):
                    q_value = max(q_value, self.getQValue(state, action))
                if q_value != float('-inf'):
                    temp_values[state] = q_value
            self.values = dict(temp_values)

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values.get(state, 0.0)
    
    def getQValue(self, state, action):
        transition = self.mdp.getTransitionStatesAndProbs(state, action)
        reward = self.mdp.getReward
        q_value = 0.0

        # Q(s, a) = T(s, a, s') * (R(s, a, s') + discount * V(s'))
        for item in transition:
            next_state, probability = item
            temp_reward = reward(state, action, next_state)
            value = self.getValue(next_state)
            q_value += probability * (temp_reward + self.discountRate * value)
        
        return q_value
    
    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)

    def getPolicy(self, state):
        ret_action = None
        max_value = float('-inf')

        for action in self.mdp.getPossibleActions(state):
            temp = self.getQValue(state, action)
            if temp > max_value:
                ret_action = action
                max_value = temp
        
        return ret_action