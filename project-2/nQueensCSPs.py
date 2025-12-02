import sys
import time
import random
from collections import deque


def is_safe_full(assignment):
    """Check if a complete assignment is a valid N-Queens solution."""
    n = len(assignment)
    for c1 in range(n):
        r1 = assignment[c1]
        for c2 in range(c1 + 1, n):
            r2 = assignment[c2]
            if r1 == r2:
                return False
            if abs(r1 - r2) == abs(c1 - c2):
                return False
    return True


# 1) Naive enumeration 

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


# 2) Backtracking + Forward Checking (MRV) 


def forward_check(domains, var, value, n, assignment):
    """
    Forward checking: remove inconsistent values from domains
    of unassigned variables after assigning var=value.
    """
    new_domains = [d.copy() for d in domains]
    consistency_checks = 0

    new_domains[var] = {value}
    assignment[var] = value

    for other in range(n):
        if other == var or assignment[other] is not None:
            continue

        to_remove = set()
        for row in new_domains[other]:
            consistency_checks += 1
            same_row = (row == value)
            same_diag = (abs(row - value) == abs(other - var))
            if same_row or same_diag:
                to_remove.add(row)

        if to_remove:
            new_domains[other] -= to_remove
            if not new_domains[other]:
                return new_domains, consistency_checks, True

    return new_domains, consistency_checks, False


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


def solve_backtracking_forward_checking(n):
    domains = [set(range(n)) for _ in range(n)]
    assignment = [None] * n
    explored_nodes = 0
    checked_assignments = 0
    consistency_checks = 0
    solution = None

    def backtrack():
        nonlocal explored_nodes, checked_assignments, consistency_checks, solution

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

            tmp_assignment = assignment[:]
            new_domains, checks, failure = forward_check(
                old_domains, var, value, n, tmp_assignment
            )
            consistency_checks += checks
            if failure:
                continue

            for i in range(n):
                domains[i] = new_domains[i].copy()
            assignment[var] = value

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
        "method": "Backtracking + Forward Checking (MRV)",
        "N": n,
        "solution": solution,
        "explored_nodes": explored_nodes,
        "checked_assignments": checked_assignments,
        "consistency_checks": consistency_checks,
        "runtime": end - start,
    }


# 3) Backtracking + AC-3 (MRV) 

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


# 4) Randomized Local Search (Min-Conflicts) 

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

        conflicted_cols = []
        for c in range(n):
            if conflicts_for_column(board, c) > 0:
                conflicted_cols.append(c)

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


# Printing helpers 

def print_board(solution):
    if solution is None:
        print("  No solution.")
        return
    n = len(solution)
    for r in range(n):
        row_chars = []
        for c in range(n):
            if solution[c] == r:
                row_chars.append("Q")
            else:
                row_chars.append(".")
        print("  " + " ".join(row_chars))


def print_result(res):
    print(f"Method: {res['method']}")
    print(f"N = {res['N']}")
    print(f"Runtime: {res['runtime']:.6f} seconds")
    print(f"Explored nodes: {res.get('explored_nodes', 'N/A')}")
    print(f"Checked assignments: {res.get('checked_assignments', 'N/A')}")
    if "valid_solutions" in res:
        print(f"Number of valid solutions: {res['valid_solutions']}")
    if "consistency_checks" in res:
        print(f"Consistency checks: {res['consistency_checks']}")
    if "ac3_checks" in res:
        print(f"AC-3 checks: {res['ac3_checks']}")
    if "steps" in res:
        print(f"Steps (local search iterations): {res['steps']}")
    print("Sample solution (if any):")
    print_board(res.get("solution"))
    print("-" * 40)


def time_str():
    return time.strftime("%H:%M:%S")


# Main
def main():
    ns = []
    for arg in sys.argv[1:]:
        if arg.lstrip("-").isdigit():
            ns.append(int(arg))
    if not ns:
        ns = [8]

    print(f"Run started at {time_str()}")

    for n in ns:
        print()
        print(f"N-Queens with N = {n}")
        print("-" * 40)

        if n <= 10:
            print(f"[{time_str()}] Running Naive enumeration...")
            naive_res = solve_naive(n)
            print_result(naive_res)
        else:
            print(
                f"[{time_str()}] Skipping Naive enumeration for N = {n} (too slow)."
            )

        print(f"[{time_str()}] Running Backtracking + Forward Checking (MRV)...")
        fc_res = solve_backtracking_forward_checking(n)
        print_result(fc_res)

        if n <= 24:
            print(f"[{time_str()}] Running Backtracking + AC-3 (MRV)...")
            ac3_res = solve_backtracking_ac3(n)
            print_result(ac3_res)
        else:
            print(
                f"[{time_str()}] Skipping Backtracking + AC-3 for N = {n} (very slow)."
            )

        print(f"[{time_str()}] Running Min-Conflicts local search...")
        mc_res = min_conflicts(n)
        print_result(mc_res)

    print(f"Run finished at {time_str()}")


if __name__ == "__main__":
    main()
