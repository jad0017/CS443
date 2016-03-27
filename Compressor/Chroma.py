import sys

from PIL import Image
from . import Matrix

def validate_spec(spec):
    A = spec.split(':')
    if len(A) != 3:
        print("Invalid Chroma Subsampling format.")
        sys.exit(1)

    try:
        a = int(A[0])
        b = int(A[1])
        c = int(A[2])
    except ValueError:
        print("Invalid Chroma Subsampling format.")
        sys.exit(1)

    if a != 4:
        print("Chroma Subsampling must use 4 for the first value.")
        sys.exit(1)

    if (not b in [0, 1, 2, 4]) or (not c in [0, 1, 2, 4]):
        print("Chroma Subsampling value must be in the set {0, 1, 2, 4}.")
        sys.exit(1)

    if (b == 0) and (c == 0):
        print("4:0:0 Chroma Subsampling is not possible.")
        sys.exit(1)

    # Not allowing these for now... not worth the effort.
    if (b == 0):
        print("4:0:x Chroma Subsampling is not possible.")
        sys.exit(1)

    return (b, c)


def chroma_subsample(M, spec):
    """
    Perform subsampling on a matrix.

    :param M: Matrix to perform sampling on.
    :param spec: Subsampling spec

    :returns: SampledMatrix: a matrix with the subsampled data
    """
    S = validate_spec(spec)

    if (S[0] == 4) and (S[1] == 4):
        return M

    A = Matrix.zero_matrix(len(M[0]), len(M))

    mod_lookup = { 4:1, 2:2, 1:4, 0:0 }
    x1mod = mod_lookup[S[0]]
    x2mod = mod_lookup[S[1]]

    V = None
    for y in range(len(M)):
        if (y % 2 == 0):
            # First row (no checking for 0 at the moment).
            for x in range(len(M[0])):
                if (x % x1mod == 0):
                    V = M[y][x]
                A[y][x] = V
        else:
            # Second row
            for x in range(len(M[0])):
                if (S[1] == 0):
                    A[y][x] = A[y - 1][x]
                elif (x % x2mod == 0):
                    V = M[y][x]
                A[y][x] = V
    return A


# vim:ts=4:sws=4:st=4:ai
