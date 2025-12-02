import time
from collections import deque

from csp_utils import is_safe_full


def constraint_ok(col_i, row_i, col_j, row_j):
    if row_i == row_j:
        return False
    if abs(row_i - row_j) == abs(col_i - col_j):
        return False
    return True


def revise(domains, xi, xj, n, metrics):
    removed = False
    to_remove = set()
    for vi in domains[xi]:
        supported = False
        for vj in domains[xj]:
            metrics["ac3_checks"] = metrics.get("ac3_checks", 0) + 1
            if constraint_ok(xi, vi, xj, vj):
                supported = True
                break
        if not supported:
            to_remove.add(vi)
    if to_remove:
        domains[xi] -= to_remove
        removed = True
    return removed


def ac3(domains, n, metrics=None):
    if metrics is None:
        metrics = {}
    metrics.setdefault("ac3_checks", 0)

    queue = deque()
    for i in range(n):
        for j in range(n):
            if i != j:
                queue.append((i, j))

    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj, n, metrics):
            if not domains[xi]:
                return False
            for xk in range(n):
                if xk != xi and xk != xj:
                    queue.append((xk, xi))
    return True


def select_unassigned_variable_mrv(domains, assignment):
    best_var = None
    best_size = None
    for var, val in enumerate(assignment):
        if val is not None:
            continue
        size = len(domains[var])
        if best_var is None or size < best_size:
            best_var = var
            best_size = size
    return best_var


def solve_backtracking_ac3(n):
    domains = [set(range(n)) for _ in range(n)]
    assignment = [None] * n
    explored_nodes = 0
    checked_assignments = 0
    metrics = {"ac3_checks": 0}
    solution = None

    def backtrack():
        nonlocal explored_nodes, checked_assignments, solution

        if all(v is not None for v in assignment):
            checked_assignments += 1
            if is_safe_full(assignment):
                solution = list(assignment)
                return True
            return False

        var = select_unassigned_variable_mrv(domains, assignment)
        if var is None:
            return False

        for value in sorted(domains[var]):
            explored_nodes += 1

            old_domains = [d.copy() for d in domains]
            old_assignment_value = assignment[var]

            assignment[var] = value
            domains[var] = {value}

            if ac3(domains, n, metrics):
                if backtrack():
                    return True

            assignment[var] = old_assignment_value
            for i in range(n):
                domains[i] = old_domains[i]

        return False

    start = time.perf_counter()
    backtrack()
    end = time.perf_counter()

    return {
        "method": "Backtracking + AC-3 (MRV)",
        "N": n,
        "solution": solution,
        "explored_nodes": explored_nodes,
        "checked_assignments": checked_assignments,
        "ac3_checks": metrics["ac3_checks"],
        "runtime": end - start,
    }


__all__ = ["solve_backtracking_ac3"]
