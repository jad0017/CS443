import math

def zero_matrix(N, M):
    """
    Generate a matrix of size NxM filled with zeros.

    :param N: Width
    :param M: Height

    :returns: A matrix of size NxM filled with zeros.
    """
    return [[0 for c in range(N)] for r in range(M)]


def zero_square_matrix(N):
    """
    Generate a square matrix of size NxN filled with zeros.

    :param N: Edge length

    :returns: A matrix of size NxN filled with zeros.
    """
    return zero_matrix(N, N)


def transpose(A):
    """
    Perform transposition on a given matrix.

    :param A: Matrix to transpose.

    :returns: The transpose matrix of :param A:.
    """
    # The transpose matrix.
    T = zero_matrix(len(A[0]), len(A))
    for j in range(len(A)):
        for i in range(len(A[0])):
            T[j][i] = A[i][j]
    return T


def multiply(A, B):
    """
    Perform matrix multiplication on two
    matraces.

    :param A:
        Matrix 1; Must have the same width as B's height.
    :param B:
        MAtrix 2; Must have the same height as A's width.

    :returns:
        The result of matrix multiplication between
        :param A: and :param B:.
    """
    C = zero_matrix(len(B[0]), len(A))
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]
    return C


def multiply_each(A, B):
    """
    Performs element-wise multiplication of
    two matraces of identical dimensions.

    :param A: Matrix 1.
    :param B: Matrix 2.

    :returns:
        The result of element-wise multiplication
        between :param A: and :param B:.
    """
    C = zero_matrix(len(A[0]), len(A))
    for i in range(len(A)):
        for j in range(len(A[0])):
            C[i][j] = A[i][j] * B[i][j]
    return C


# vim:ts=4:sts=4:sw=4:ai:et
