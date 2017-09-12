import itertools
import copy

class GameState:

    def __init__(self):
        self.initiative = 0
        self.width = 3
        self.height = 2
        xs = list(range(self.width))
        ys = list(range(self.height))
        self.board = [ [ '' for y in ys] for x in xs ]
        self.board[2][1] = '/'
        self.cells = [ (x,y) for y in ys for x in xs ]
        self.players = [None,None]
    
    def forecast_move(self, move):
        """ Return a new board object with the specified move
t        applied to the current game state.
        
        Parameters
        ----------
        move: tuple
            The target position for the active player's next move
        """
        cpy = copy.deepcopy(self)
        cpy.board[move[0]][move[1]] = 'X'
        cpy.players[self.initiative] = move
        cpy.initiative = (cpy.initiative + 1) % 2
        return cpy
    
    def isOpen(self, cell):
        return not self.board[cell[0]][cell[1]]

    def print(self):
        xs = list(range(self.width))
        ys = list(range(self.height))
        def val(x):
          if not x: return ' '
          return x
        for y in ys:
            line = '|' + '|'.join([ val(self.board[x][y]) for x in xs ]) + '|'
            print(line)
            print('-' * self.width * 2)
      
    
    def get_legal_moves(self):
        """ Return a list of all legal moves available to the
        active player.  Each player should get a list of all
        empty spaces on the board on their first move, and
        otherwise they should get a list of all open spaces
        in a straight line along any row, column or diagonal
        from their current position. (Players CANNOT move
        through obstacles or blocked squares.) Moves should
        be a pair of integers in (column, row) order specifying
        the zero-indexed coordinates on the board.
        """
        if not all(self.players):
            return [ cell for cell in self.cells if self.isOpen(cell) ]
        loc = self.players[self.initiative]
        def march(loc,dx,dy):
            i = 1
            while True:
                loc = (loc[0] + dx, loc[1] + dy)
                if loc[0] < 0 or loc[1] < 0 or loc[0] >= self.width or loc[1] >= self.height: return
                if not self.isOpen(loc): return
                yield loc
          
        return list(itertools.chain( march(loc,-1,0)
        , march(loc, 1,0) 
        , march(loc,0,-1) 
        , march(loc,0,1) 
        , march(loc,-1,-1) 
        , march(loc,1,-1) 
        , march(loc,1,1) 
        , march(loc,-1,1) ))
