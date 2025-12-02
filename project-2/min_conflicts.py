import random
import time


def conflicts_for_column(board, col):
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
    board = [random.randrange(n) for _ in range(n)]
    explored_nodes = 0
    checked_assignments = 0

    start = time.perf_counter()

    for step in range(max_steps):
        checked_assignments += 1

        conflicted_cols = [c for c in range(n) if conflicts_for_column(board, c) > 0]

        if not conflicted_cols:
            end = time.perf_counter()
            return {
                "method": "Min-Conflicts local search",
                "N": n,
                "solution": list(board),
                "explored_nodes": explored_nodes,
                "checked_assignments": checked_assignments,
                "steps": step,
                "runtime": end - start,
            }

        col = random.choice(conflicted_cols)

        best_rows = []
        best_conf = None
        for row in range(n):
            explored_nodes += 1
            conf = 0
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

        board[col] = random.choice(best_rows)

    end = time.perf_counter()
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
