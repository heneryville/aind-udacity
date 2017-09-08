assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # twins are pairs in the same unit that share possibilties of length 2
    twins = [ pair for pair in unit_pairs if values[pair[0]] == values[pair[1]] and len(values[pair[0]]) == 2 ]
    # Eliminate the naked twins as possibilities for their peers
    for twin in twins:
        for box in unitlist[twin[2]]:
            if box == twin[0] or box == twin[1]: continue # Don't eliminate the twins themselves!
            for digit in values[twin[0]]:
                assign_value(values,box, values[box].replace(digit,''))
    return values

def combos(A):
    """
    All unique pairs of elements in A.
    e.g. if A is [1,2,3], then the result is [(1,2),(1,3),(2,3)]
    """
    for i in range(len(A)):
        for j in range(i+1,len(A)):
            yield (A[i],A[j])

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    def normalize(c):
        """ Converts a dot to all possibilities, otherwise it's what we got"""
        if c=='.': return cols
        return c
    return { x[0]: normalize(x[1]) for x in zip(boxes,grid) }

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Go through all the boxes, and choose which values it can have based on peers that are already known.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1] # All boxes that have been solved
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]: # Eliminate that value in peers
            values[peer] = values[peer].replace(digit,'')

    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        groups = {num: [] for num in cols} # Groups cells with a given possibility.
        for cell in unit:
            for l in values[cell]: groups[l].append(cell)
        for num,group in groups.items():
            if len(group) != 1: continue #If we've got a group of size zero, it's a bad grid, but we'll discover that soon in reduce
            values[group[0]] = num
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after # We'ved stalled if we've made no change in solved boxes
        if len([box for box in values.keys() if len(values[box]) == 0]): # When a box has no options, we messed up. No solution here
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False: return False
    # Choose one of the unfilled squares with the fewest possibilities
    unsolved = [(len(values[c]), c) for c in values.keys() if len(values[c]) > 1 ]
    if len(unsolved) == 0:  return values
    n,cell = min(unsolved)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for possibility in values[cell]:
        vCopy = values.copy() # We're mutating values, so copy it for each branch
        vCopy[cell] = possibility
        solution = search(vCopy)
        if solution != False: return solution
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)

    return search(values)

def validate(values):
    for unit in unitlist:
        used = [ values[x] for x in unit ]
        if len(used) != 9: raise Exception('Unit has wrong length')
        if ''.join(sorted(used)) != cols: raise Exception('Unit has duplicate values: ' + ','.join(sorted(used)) + '\n Unit: ' + str(unit))

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
forward_diag = [ s[0] + s[1] for s in zip(rows,cols) ]
backward_diag = [ s[0] + s[1] for s in zip(rows,reversed(cols)) ]

unitlist = row_units + column_units + square_units + [ forward_diag, backward_diag ]
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
unit_pairs = [ x + (i,) for i in range(len(unitlist)) for x in combos(unitlist[i])]

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid_2 = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    solution = solve(diag_sudoku_grid_2)
    display(solution)
    validate(solution)

    print('Done running')
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit as e:
        print('Could not import visualize due to system exception')
        print(e)
        pass
    except Exception as e:
        print('Could not import visualize')
        print(e)
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
