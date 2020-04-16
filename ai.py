def maxvalue(state, gameover, score, agentActions, gameActions, result, depth):
    if gameover(state):
        return 0, None
    elif depth == 0:
        return score(state), None
    value, bestAction = float("-inf"), None
    for action in agentActions(state):
        nextState = result(state, action)
        nextValue, _ = expectedvalue(nextState, gameover, score, agentActions, gameActions, result, depth - 1)
        if nextValue > value:
            value, bestAction = nextValue, action
    return value, bestAction

def expectedvalue(state, gameover, score, agentActions, gameActions, result, depth):
    """
    Returns the tuple (score, bestMove).
    """
    if len(gameActions(state)) == 0 or depth == 0:
        return score(state), None
    
    total = 0.0
    total_weights = 0.0
    for action, probability in gameActions(state):
        nextState = result(state, action) 
        nextValue, _ = maxvalue(nextState, gameover, score, agentActions, gameActions, result, depth)
        total += nextValue * probability
        total_weights += probability

    return total / total_weights, None

def expectimax(state, gameover, score, agentActions, gameActions, result, depth):
    return maxvalue(state, gameover, score, agentActions, gameActions, result, depth)[1]
