import heapq
from isolation import Board

def reachability(game,loc,limit=99):
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
            for v2 in game.get_moves(v1):
                heapq.heappush(q,(cost+1,v2))
    return grid

def compute_reachability(width,height,loc,limit=99):
    game = Board("p1", "p2",width,height)
    print(reachability(game,loc,limit).to_string())

def opposed_reachability(game,loc_p1,loc_p2,limit=99):
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
            for v2 in game.get_moves(v1):
                heapq.heappush(q,(cost+1,p2,v2))
    return grid

class CostGrid:
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

def main():
    print(compute_reachability(7,7,(0,0),3)._board)

if __name__ == "__main__":
    main()
