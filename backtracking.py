from typing import List, Set

def backtracking(N: int):
    board = [-1] * N
    domains = [set(range(N)) for _ in range(N)]
    metrics = {"expansions": 0, "consistency": 0}

    isSolved = rec_backtracking(board, domains, N, 0, metrics)

    return {
        "solution": board if isSolved else None,
        "metrics": metrics
    }

def rec_backtracking(board: List[int], domains: List[Set[int]], N: int,
                     assigned_count: int, metrics: dict) -> bool:

    if assigned_count == N:
        return True

    var = mrv(board, domains, N)
    metrics["expansions"] += 1

    for value in list(domains[var]):

        if is_consistent(board, var, value):
            board[var] = value
            domain_copy = [d.copy() for d in domains]

            ok, new_domains = fwd_checking(var, value, board, domain_copy, N, metrics)

            if ok:
                if rec_backtracking(board, new_domains, N, assigned_count + 1, metrics):
                    return True

            board[var] = -1

    return False

def mrv(board: List[int], domains: List[Set[int]], N: int) -> int:
    best_var = None
    best_size = N + 1

    for r in range(N):
        if board[r] == -1:
            size = len(domains[r])
            if size < best_size:
                best_size = size
                best_var = r
    return best_var

def is_consistent(board: List[int], row: int, col: int) -> bool:
    for r in range(row):
        c = board[r]
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

def fwd_checking(row: int, col: int, board: List[int], domains: List[Set[int]],
                 N: int, metrics: dict):
    
    for next_row in range(row + 1, N):
        for value in list(domains[next_row]):

            metrics["consistency"] += 1

            conflict = (
                value == col or
                abs(value - col) == abs(next_row - row)
            )

            if conflict:
                domains[next_row].remove(value)

        if not domains[next_row]:
            return False, domains

    return True, domains

def visualize_board(N: int, solution: List[int]):
    for r in range(N):
        print(" ".join("Q" if solution[r] == c else "." for c in range(N)))

def main():
    Ns = [4, 8, 16, 32]

    # Proper for-loop
    for N in Ns:
        print(f"\n--- Solving N = {N} ---")

        result = backtracking(N)

        solution = result["solution"]
        metrics = result["metrics"]

        if solution:
            visualize_board(N, solution)
        else:
            print("No solution found.")

        print("Metrics:", metrics)

if __name__ == "__main__":
    main()
