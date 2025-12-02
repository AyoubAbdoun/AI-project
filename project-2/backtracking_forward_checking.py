import time

from csp_utils import is_safe_full


def forward_check(domains, var, value, n, assignment):
    """Forward checking to prune inconsistent values after assigning var=value."""
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
            same_row = row == value
            same_diag = abs(row - value) == abs(other - var)
            if same_row or same_diag:
                to_remove.add(row)

        if to_remove:
            new_domains[other] -= to_remove
            if not new_domains[other]:
                return new_domains, consistency_checks, True

    return new_domains, consistency_checks, False


def select_unassigned_variable_mrv(domains, assignment):
# Pick the column that has the fewest legal rows left
# Because that column is the hardest one, solving it first reduces backtracking
    best_var = None
    best_size = None
    # var = column index
    # val = row or None (if not assigned)
    for var, val in enumerate(assignment):
        if val is not None:
            continue # If this column already has a queen, ignore it
        
        # how many options are left
        # domains[var] = set of allowed rows
        size = len(domains[var])

        if best_var is None or size < best_size:
            best_var = var
            best_size = size
    return best_var


def solve_backtracking_forward_checking(n):
    # create one domain per column
    # initially every column can place a queen in every row
    # forward checking will shrink these sets as we assign queens
    domains = [set(range(n)) for _ in range(n)]
    assignment = [None] * n # build the current partial assignment list
    explored_nodes = 0
    checked_assignments = 0
    consistency_checks = 0
    solution = None

    def backtrack():
        nonlocal explored_nodes, checked_assignments, consistency_checks, solution

        # check whether the search has reached a full assignment
        # all(...) checks if every column has an assigned row
        if all(v is not None for v in assignment):
            checked_assignments += 1
            if is_safe_full(assignment):
                solution = list(assignment) # assignment[col] = row
                return True
            return False

        var = select_unassigned_variable_mrv(domains, assignment)
        if var is None:
            return False # no legal rows

        # For this column, try every row that is still allowed, one by one
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


__all__ = ["solve_backtracking_forward_checking"]
