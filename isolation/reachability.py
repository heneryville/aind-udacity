import heapq

def reachability(game,loc):
    cellCount = game.width * game.height
    grid = CostGrid(game.width,game.height)
    q = [ (0,loc) ]
    seen = set()

    while q:
        (cost,v1) = heapq.heappop(q)
        if v1 not in seen:
            seen.add(v1)
            grid.set(v1,cost)
            if len(seen) == cellCount: return grid
            for v2 in game.get_moves(v1):
                heapq.heappush(q,(cost+1,v2))
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

    def pairs(self):
        for x in range(self.width):
            for y in range(self.height):
                loc = (y,x)
                yield (self.at(loc),loc)

    def values(self):
        return self._board
