from gamestate import *

def terminal_test(gameState):
    """ Return True if the game is over for the active player
    and False otherwise.
    """
    return len(gameState.get_legal_moves()) == 0



def min_value(gameState):
    """ Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """
    if terminal_test(gameState): return 1
    return min( max_value(gameState.forecast_move(move)) for move in gameState.get_legal_moves() )


def max_value(gameState):
    """ Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal child
    nodes.
    """
    if terminal_test(gameState): return -1

def minimax(gameState):
    if gameState.initiative == 0:
        return min([( max_value(gameState.forecast_move(move)), move) for move in gameState.get_legal_moves()])[1]
    else:
        return max([( min_value(gameState.forecast_move(move)), move) for move in gameState.get_legal_moves()])[1]
