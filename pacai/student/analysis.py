"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    The optimal policy wants the agent to cross the bridge fully,
    so setting the noise to 0.0 allows the optimal policy to be followed without fail
    """

    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise

def question3a():
    """
    Raise living reward to high enough value where the algorithm
    would rather risk falling into the cliff than take the long way
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = -1

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    Keep the same living reward as part a, but reduce noise to 0
    """

    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = -1

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    Increase noise to 0.3, optimal policy prefers slow route but there's still a chance
    for the agent to risk the bridge if unlucky
    """

    answerDiscount = 0.9
    answerNoise = 0.3
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    Keep living reward at 0 to prioritize safely getting to the exit
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    Set living reward to high value to reward agent for prolonging the game and not exiting
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 100

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    It is not possible to have a 99% probability of visiting every state if given 50 iterations
    """

    # answerEpsilon = 0.3
    # answerLearningRate = 0.5

    return NOT_POSSIBLE

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
