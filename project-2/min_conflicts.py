import random
import time


def conflicts_for_column(board, col):
    """Count how many attacking queens the queen in column col currently has."""
    n = len(board)
    row = board[col]
    conflicts = 0
    for c in range(n):
        if c == col:
            continue
        r2 = board[c]
        if r2 == row or abs(r2 - row) == abs(c - col):
            conflicts += 1
    return conflicts


def min_conflicts(n, max_steps=100000):
    board = [random.randrange(n) for _ in range(n)] # start with a random row for every column
    explored_nodes = 0
    checked_assignments = 0

    start = time.perf_counter()

    for step in range(max_steps): # perform up to max_steps repair iterations
        checked_assignments += 1

        # Track which columns currently violate constraints
        conflicted_cols = [c for c in range(n) if conflicts_for_column(board, c) > 0]

        if not conflicted_cols:
            end = time.perf_counter()
            # board is a valid solution because no queens threaten each other
            return {
                "method": "Min-Conflicts local search",
                "N": n,
                "solution": list(board),
                "explored_nodes": explored_nodes,
                "checked_assignments": checked_assignments,
                "steps": step,
                "runtime": end - start,
            }

        col = random.choice(conflicted_cols) # pick one conflicted queen to move

        best_rows = []
        best_conf = None
        for row in range(n):
            explored_nodes += 1
            conf = 0
            # Count conflicts if this queen is moved to 'row'
            for c2 in range(n):
                if c2 == col:
                    continue
                r2 = board[c2]
                if r2 == row or abs(r2 - row) == abs(c2 - col):
                    conf += 1
            if best_conf is None or conf < best_conf:
                best_conf = conf
                best_rows = [row]
            elif conf == best_conf:
                best_rows.append(row)

        # Move the queen to one of the rows with minimum conflicts (ties broken uniformly)
        board[col] = random.choice(best_rows)

    end = time.perf_counter()
    # Ran out of steps without finding a conflict-free assignment
    return {
        "method": "Min-Conflicts local search",
        "N": n,
        "solution": None,
        "explored_nodes": explored_nodes,
        "checked_assignments": checked_assignments,
        "steps": max_steps,
        "runtime": end - start,
    }


__all__ = ["min_conflicts"]
