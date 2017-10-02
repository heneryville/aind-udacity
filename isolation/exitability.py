import reachability
from isolation import Board
from reachability import CostGrid


def compute_exitability(width,height):
    game = Board("p1", "p2",width,height)
    grid = CostGrid(width,height)
    for x in range(game.width):
        for y in range(game.height):
            #print(y,x,len(game.get_moves((y,x))))
            grid.set((y,x),len(game.get_moves((y,x))))
    return grid

EXIT_7x7 = [2, 3, 4, 4, 4, 3, 2, 3, 4, 6, 6, 6, 4, 3, 4, 6, 8, 8, 8, 6, 4, 4, 6, 8, 8, 8, 6, 4, 4, 6, 8, 8, 8, 6, 4, 3, 4, 6, 6, 6, 4, 3, 2, 3, 4, 4, 4, 3, 2]

def exitability(loc):
    return EXIT_7x7[loc[0] + loc[1] * 7]

def main():
    print(compute_exitability(7,7)._board)
    return

if __name__ == "__main__":
    main()
