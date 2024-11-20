from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import probability
from pacai.util import reflection

import random
import numpy as np

class QLearningAgent(ReinforcementAgent):
    """
    A Q-Learning agent.

    Some functions that may be useful:

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getAlpha`:
    Get the learning rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getDiscountRate`:
    Get the discount rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`:
    Get the exploration probability.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getLegalActions`:
    Get the legal actions for a reinforcement agent.

    `pacai.util.probability.flipCoin`:
    Flip a coin (get a binary value) with some probability.

    `random.choice`:
    Pick randomly from a list.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Compute the action to take in the current state.
    With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
    we should take a random action and take the best policy action otherwise.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should choose None as the action.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    The parent class calls this to observe a state transition and reward.
    You should do your Q-Value update here.
    Note that you should never call this function, it will be called on your behalf.

    DESCRIPTION: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

        # You can initialize Q-values here.
        self.q_values = {}

    def getQValue(self, state, action):
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """
        pair = (state, action)
        return self.q_values.get(pair, 0.0)

    def getValue(self, state):
        """
        Return the value of the best action in a state.
        I.E., the value of the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of 0.0.

        This method pairs with `QLearningAgent.getPolicy`,
        which returns the actual best action.
        Whereas this method returns the value of the best action.
        """

        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return 0.0
        max_q = float('-inf')
        for action in actions:
            max_q = max(max_q, self.getQValue(state, action))
        
        return max_q

    def getPolicy(self, state):
        """
        Return the best action in a state.
        I.E., the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of None.

        This method pairs with `QLearningAgent.getValue`,
        which returns the value of the best action.
        Whereas this method returns the best action itself.
        """

        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return None
        
        best_action = None
        best_q = float('-inf')

        for action in actions:
            temp_q = self.getQValue(state, action)
            if temp_q > best_q:
                best_action = action
                best_q = temp_q
        
        return best_action

    def update(self, state, action, nextState, reward):
        discount = self.getDiscountRate()
        alpha = self.getAlpha()
        max_q = self.getValue(nextState)
        sample = reward + (discount * max_q)
        current_q = self.getQValue(state, action)

        # Q(s, a) = (1 - alpha) * Q(s, a) + (alpha * sample)
        current_q = (1 - alpha) * current_q + (alpha * sample)
        self.q_values[(state, action)] = current_q
    
    def getAction(self, state):
        # Flip coin based on exploration probability
        coin = probability.flipCoin(self.getEpsilon())
        actions = self.getLegalActions(state)
        ret = None
        if coin:
            ret = random.choice(actions)
        else:
            ret = self.getPolicy(state)
        
        return ret

class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as `QLearningAgent`, but with different default parameters.
    """

    def __init__(self, index, epsilon = 0.05, gamma = 0.8, alpha = 0.2, numTraining = 0, **kwargs):
        kwargs['epsilon'] = epsilon
        kwargs['gamma'] = gamma
        kwargs['alpha'] = alpha
        kwargs['numTraining'] = numTraining

        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Simply calls the super getAction method and then informs the parent of an action for Pacman.
        Do not change or remove this method.
        """

        action = super().getAction(state)
        self.doAction(state, action)

        return action

class ApproximateQAgent(PacmanQAgent):
    """
    An approximate Q-learning agent.

    You should only have to overwrite `QLearningAgent.getQValue`
    and `pacai.agents.learning.reinforcement.ReinforcementAgent.update`.
    All other `QLearningAgent` functions should work as is.

    Additional methods to implement:

    `QLearningAgent.getQValue`:
    Should return `Q(state, action) = w * featureVector`,
    where `*` is the dotProduct operator.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    Should update your weights based on transition.

    DESCRIPTION: 
    """

    def __init__(self, index,
            extractor = 'pacai.core.featureExtractors.IdentityExtractor', **kwargs):
        super().__init__(index, **kwargs)
        self.featExtractor = reflection.qualifiedImport(extractor)

        # You might want to initialize weights here.
        self.weights = {}

    def getQValue(self, state, action):
        features = self.featExtractor.getFeatures(self, state, action)
        ret = 0.0

        for feature in features:
            if feature not in self.weights:
                continue
            weight = self.weights[feature]
            ret += weight * features[feature]

        return ret
        
    def update(self, state, action, nextState, reward):
        discount = self.getDiscountRate()
        alpha = self.getAlpha()
        value = self.getValue(nextState)
        q_value = self.getQValue(state, action)
        features = self.featExtractor.getFeatures(self, state, action)
        correction = (reward + discount * value) - q_value
        # 𝑤←𝑤+𝛼[𝑐𝑜𝑟𝑟𝑒𝑐𝑡𝑖𝑜𝑛]𝑓𝑖(𝑠,𝑎)
        # 𝑐𝑜𝑟𝑟𝑒𝑐𝑡𝑖on=(𝑅(𝑠,𝑎)+𝛾𝑉′(𝑠))−𝑄(𝑠,𝑎)
        for feature in features:
            self.weights[feature] = self.weights.get(feature, 0.0) + alpha * correction * features[feature] 

    def final(self, state):
        """
        Called at the end of each game.
        """
        alpha = self.getAlpha()
        # Call the super-class final method.
        super().final(state)

        # Did we finish training?
        if self.episodesSoFar == self.numTraining:
            # You might want to print your weights here for debugging.
            # *** Your Code Here ***
            pass
