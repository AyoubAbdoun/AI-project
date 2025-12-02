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


__all__ = ["is_safe_full"]
