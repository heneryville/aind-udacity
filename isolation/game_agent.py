"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math
import heapq
from isolation import Board

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

# A list of some negative powers of 2 so I don't have to re-compute them. NEG_POWERS[i] = 2**-i
NEG_POWERS = [1,.5,.25,.125,.0625,.03125]

def opposed_reachable(game,player):
    LIMIT = 3
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    if game.active_player == player:
        grid = opposed_reachability(game,game.get_player_location(player),game.get_player_location(game.get_opponent(player)),LIMIT)
    else:
        grid = opposed_reachability(game,game.get_player_location(game.get_opponent(player)),game.get_player_location(player),LIMIT)
        grid.negate()

    pValues = sum ( NEG_POWERS[int(dist)] for dist in grid.values() if dist > 0 and dist <= LIMIT )
    oValues = sum ( NEG_POWERS[-int(dist)] for dist in grid.values() if dist < 0 and dist >= -LIMIT ) # Opponents scores will be negative, so this is the difference between reachability

    return pValues - oValues

def reachable_diff(game,player):
    LIMIT = 3
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    def reachability_score(player):
        grid = reachability(game,game.get_player_location(player),LIMIT)
        return sum ( NEG_POWERS[int(dist)] for dist in grid.values() if dist <= LIMIT  )
    return reachability_score(player) - reachability_score(game.get_opponent(player))

def weighted_precomputed_move_advantage_with_initiative(game,player):
    own_moves = set(game.get_legal_moves(player))
    opp_moves = set(game.get_legal_moves(game.get_opponent(player)))
    if player == game.active_player and not len(own_moves):
        return float("-inf")
    if player != game.active_player and not len(opp_moves):
        return float("inf")

    if player == game.active_player:
        opp_moves = opp_moves - own_moves
    else:
        own_moves = own_moves - opp_moves

    def get_weighted_moves(moves):
        return sum( exitability(move) for move in moves )

    return float( get_weighted_moves(own_moves) - get_weighted_moves(opp_moves)  )

def weighted_precomputed_move_advantage(game,player):
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    if player == game.active_player and not len(own_moves):
        return float("-inf")
    if player != game.active_player and not len(opp_moves):
        return float("inf")

    def get_weighted_moves(moves):
        return sum( exitability(move) for move in moves )

    return float( get_weighted_moves(own_moves) - get_weighted_moves(opp_moves)  )

def weighted_move_advantage(game,player):
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    if player == game.active_player and not len(own_moves):
        return float("-inf")
    if player != game.active_player and not len(opp_moves):
        return float("inf")

    def get_weighted_moves(moves):
        return sum( len(game.get_moves(move)) for move in moves )

    return float( get_weighted_moves(own_moves) - get_weighted_moves(opp_moves)  )


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    return weighted_precomputed_move_advantage_with_initiative(game,player)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    return reachable_diff(game,player)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    return opposed_reachable(game,player)



class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        #print('####minimax### @ ',depth)
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        score, path = self.maxvalue(game,depth, [])
        #print('Best path',score,path)
        if not path: return (-1,-1)
        return path[0]

    def maxvalue(self, game, depth, inpath):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()
        if self.terminal_test(game,moves,depth):
          score = self.score(game,self)
          #print('-'*(self.search_depth - depth) ,'max',score,inpath)
          return (score,inpath)
        nexts = ( self.minvalue(game.forecast_move(move),depth-1, inpath + [move]) for move in moves )
        val, path = max(nexts)
        #print('-'*(self.search_depth - depth) ,'max',val,inpath)
        return (val, path)

    def minvalue(self,game, depth, inpath):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()
        if self.terminal_test(game,moves,depth):
          score = self.score(game,self)
          #print('-'*(self.search_depth - depth) ,'min',score,inpath)
          return (score,inpath)
        nexts = ( self.maxvalue(game.forecast_move(move),depth-1, inpath  + [move]) for move in moves )
        val, path = min(nexts)
        #print('-'*(self.search_depth - depth) ,'min',val,inpath)
        return (val,path)

    def terminal_test(self, game, moves, depth):
        if depth <= 0: return True
        return len(moves) <= 0



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=20.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.depths_reached = []

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        depth = 0

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while True:
                depth = depth + 1
                best_move = self.alphabeta(game, depth)
            print("Got move on depth limit, with depth of ", self.search_depth)
            return best_move

        except SearchTimeout:
            # Return the best move from the last completed search iteration
            print("Got move on time, with depth of ", depth)
            self.depths_reached.append(depth)
            return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        score, path = self.maxvalue(game,depth,float("-inf"),float("inf"),[])
        if not path: return (-1,-1)
        return path[0]

    def maxvalue(self, game, depth, alpha, beta, inpath):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()
        if self.terminal_test(game,moves,depth):
            score = self.score(game,self)
            #print('-'*(self.search_depth - depth) ,'max',score,inpath)
            return (score,inpath)
        mval = float("-inf")
        mpath = None
        for move in moves:
            moved = game.forecast_move(move)
            nval, npath = self.minvalue(moved,depth-1,alpha,beta,inpath + [move])
            if not mpath: mpath = npath
            if nval > mval:
                mval = nval
                mpath = npath
            if nval >= beta: return (mval,mpath)
            alpha = max(alpha,nval)
        return (mval, mpath)

    def minvalue(self,game, depth, alpha, beta, inpath):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        moves = game.get_legal_moves()
        if self.terminal_test(game,moves,depth):
          score = self.score(game,self)
          #print('-'*(self.search_depth - depth) ,'min',score,inpath)
          return (score,inpath)
        mval = float("inf")
        mpath = None
        for move in moves:
            moved = game.forecast_move(move)
            nval, npath = self.maxvalue(moved,depth-1,alpha,beta,inpath + [move])
            if not mpath: mpath = npath
            if nval < mval:
                mval = nval
                mpath = npath
            if nval <= alpha: return (mval,mpath)
            beta = min(beta,nval)
        return (mval, mpath)

    def terminal_test(self, game, moves, depth):
        return depth <= 0 or len(moves) <= 0



#*****************
#* The below code is copied from other files since the auto-grader does not accept multiple files
#*****************

# Defines on a 7x7 board how many possible moves there are from each square. In (y,x) => y + x * h notation
EXIT_7x7 = [2, 3, 4, 4, 4, 3, 2, 3, 4, 6, 6, 6, 4, 3, 4, 6, 8, 8, 8, 6, 4, 4, 6, 8, 8, 8, 6, 4, 4, 6, 8, 8, 8, 6, 4, 3, 4, 6, 6, 6, 4, 3, 2, 3, 4, 4, 4, 3, 2]

def exitability(loc):
    return EXIT_7x7[loc[0] + loc[1] * 7]

def reachability(game,loc,limit=99):
    """
    Dijkstra' algoritim. Will search for all nodes reachable from loc on game (depth limited) and returns a grid with the number of moves to reach each.
    Unreachable nodes will return infinity, and the starting node will be 0
    """
    cellCount = game.width * game.height
    grid = CostGrid(game.width,game.height)
    q = [ (0,loc) ]
    seen = set()

    while q:
        (cost,v1) = heapq.heappop(q)
        if v1 not in seen:
            seen.add(v1)
            if cost > limit: return grid
            grid.set(v1,cost)
            if len(seen) == cellCount: return grid
            for v2 in game._Board__get_moves(v1): # I wish board had non-private access to it's get_moves from a location!
                heapq.heappush(q,(cost+1,v2))
    return grid

def opposed_reachability(game,loc_p1,loc_p2,limit=99):
    """
    Dijkstra' algoritim but seeded with two starting nodes. This will return a cost grid with positive values being cells reached by player 1 first,
    and negative values being cells reached by player 2 first. Nodes that are equal distant will be given to player 1, so ensure that is the player with initiative.
    """
    cellCount = game.width * game.height
    grid = CostGrid(game.width,game.height)
    q = [ (0,False,loc_p1), (0,True,loc_p2) ] #The player that has initiative should get get to reach all cells first in case of a tie
    seen = set()

    while q:
        cost,p2,v1 = heapq.heappop(q)
        if v1 not in seen:
            seen.add(v1)
            if cost > limit: return grid
            if p2: grid.set(v1,-cost)
            else: grid.set(v1,cost)
            if len(seen) == cellCount: return grid
            for v2 in game._Board__get_moves(v1):  # I wish board had non-private access to it's get_moves from a location!
                heapq.heappush(q,(cost+1,p2,v2))
    return grid

class CostGrid:
    """
    A grid that holds a value in each square. Used to evaluate dijkstra's algo
    """
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self._board = [float("inf")] * (width*height)

    def at(self,loc):
        return self._board[loc[0] + loc[1] * self.height]

    def set(self,loc,cost):
        self._board[loc[0] + loc[1] * self.height] = cost

    def negate(self):
        for i in range(len(self._board)):
            self._board[i] = - self._board[i]

    def pairs(self):
        for x in range(self.width):
            for y in range(self.height):
                loc = (y,x)
                yield (self.at(loc),loc)

    def values(self):
        return self._board

    def to_string(self):
        """Generate a string representation of the current game state, marking
        the location of each player and indicating which cells have been
        blocked, and which remain open.
        """
        col_margin = len(str(self.height - 1)) + 1
        prefix = "{:<" + "{}".format(col_margin) + "}"
        offset = " " * (col_margin + 3)
        out = offset + '   '.join(map(str, range(self.width))) + '\n\r'
        for i in range(self.height):
            out += prefix.format(i) + ' | '
            for j in range(self.width):
                idx = i + j * self.height
                out += str(self._board[idx])
                out += ' | '
            out += '\n\r'

        return out
