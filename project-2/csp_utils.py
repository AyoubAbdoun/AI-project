# takes a complete board assignment
# checks if any two queens attack each other
def is_safe_full(assignment):
    """Check if a complete assignment is a valid N-Queens solution."""
    n = len(assignment)

    # Loop over each queen by its column c1
    for c1 in range(n):
        r1 = assignment[c1] # row of queen in c1

        # Compare queen of c1 with every queen after it (c2)
        for c2 in range(c1 + 1, n):
            r2 = assignment[c2]
            
            # row conflict
            if r1 == r2:
                return False
            
            # diagonal conflict
            if abs(r1 - r2) == abs(c1 - c2):
                return False
    return True

# expose the module(s) for wildcard imports (from csp_utils import *) 
__all__ = ["is_safe_full"]
