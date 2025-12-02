import sys
import time

from backtracking_ac3 import solve_backtracking_ac3
from backtracking_forward_checking import solve_backtracking_forward_checking
from min_conflicts import min_conflicts
from naive_enumeration import solve_naive


# Printing helpers

def print_board(solution):
    if solution is None:
        print("  No solution.")
        return
    n = len(solution)
    for r in range(n):
        row_chars = []
        for c in range(n):
            # Is the queen in column c placed in row r?
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
    # read command-line arguments and  collect all valid integer args
    for arg in sys.argv[1:]:
        if arg.lstrip("-").isdigit():
            ns.append(int(arg))
    if not ns: # list is empty
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
