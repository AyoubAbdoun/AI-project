import time

from csp_utils import is_safe_full


def solve_naive(n):
    board = [0] * n
    explored_nodes = 0
    checked_assignments = 0
    valid_solutions = 0
    first_solution = None

    def backtrack(col):
        nonlocal explored_nodes, checked_assignments, valid_solutions, first_solution
        if col == n:
            checked_assignments += 1
            if is_safe_full(board):
                valid_solutions += 1
                if first_solution is None:
                    first_solution = list(board)
            return

        for row in range(n):
            board[col] = row
            explored_nodes += 1
            backtrack(col + 1)

    start = time.perf_counter()
    backtrack(0)
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
