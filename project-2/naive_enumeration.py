import time

from csp_utils import is_safe_full


def solve_naive(n):
    board = [0] * n # set the board to a list of n zeros
    explored_nodes = 0 
    checked_assignments = 0
    valid_solutions = 0
    first_solution = None

    # fill the board column by column.
    # Columns are numbered 0 to n-1
    # Every recursive call handles one colum.
    # For the current column col,try every possible row and recurse to the next column.
    def backtrack(col):
        # modify variables from the nearest enclosing function (solve_naive)
        nonlocal explored_nodes, checked_assignments, valid_solutions, first_solution
        
        # base case: all columns filled
        if col == n:
            checked_assignments += 1
            if is_safe_full(board):
                valid_solutions += 1
                if first_solution is None:
                    first_solution = list(board)
            return
        
        # Recursive case: try all rows for this column
        for row in range(n):
            board[col] = row
            explored_nodes += 1 # one attempted placement
            backtrack(col + 1)

    start = time.perf_counter()
    backtrack(0) # start by placing a queen in col 0
    end = time.perf_counter()

    return {
        "method": "Naive enumeration",
        "N": n,
        "solution": first_solution,
        "valid_solutions": valid_solutions,
        "explored_nodes": explored_nodes,
        "checked_assignments": checked_assignments,
        "runtime": end - start,
    }


__all__ = ["solve_naive"]
