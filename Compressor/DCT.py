import math
# Local imports
import Matrix


def generate_DCT_matrix(N):
    """
    Generate the DCT matrix based off the following
    equation:
             { 1 / sqrt(N)                                    if i = 0
    T(i,j) = {
             { sqrt((2 / N) * cos((i * pi * (2j + 1)) / 2N))  if i > 0

    :param N: Matrix edge length

    :returns: The DCT translation matrix.
    """
    T = [ ] # Empty array of rows
    # Create the first row which is all 1 / sqrt(N).
    T.append( [ float(1.0 / math.sqrt(N)) ] * N )
    m = float(2.0 * N)
    sd = math.sqrt( float(2.0 / N) )
    # Compute the remaining N-1 rows..
    for i in range(1, N): # range = [a,b)
        A = [ 0 ] * N
        for j in range(0, N):
            A[j] = sd * math.cos( float(math.pi * i * (2 * j +  1)) / m )
        T.append( A )
    return T

# Globals for size 8.
# TODO: Make this a dictionary cache.
DCT_T8 = generate_DCT_matrix(8)
DCT_Tp8 = Matrix.transpose(DCT_T8)


def DCT(M):
    """
    Perform The Discrete Cosine Transform on
    a given square matrix.

    :param M: Matrix to perform DCT on.

    :returns: The matrix result of DCT.
    """
    # If length of M is 8, use the
    # pre-generated matrices.
    if len(M) == 8:
        global DCT_T8
        global DCT_Tp8
        T = DCT_T8
        TT = DCT_Tp8
    else:
        T = generate_DCT_matrix(len(M))
        TT = Matrix.transpose(T)
    # D = T M T'
    A = Matrix.multiply(T, M)
    return Matrix.multiply(A, TT)


def multiply_and_adjust(A, B):
    """
    Used by :function iDCT:.
    Peroforms the following function:
    C = round(AB) + 128
    This is an optimization instead of
    doing a multiply followed by
    additional iterations for the
    rounding and adjustment.

    :param A: Matrix 1 to multiply.
    :param B: Matrix 2 to multiply.

    :returns: The result of the above equation.
    """
    C = Matrix.zero_matrix(len(B[0]), len(A))
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]
            C[i][j] = round(C[i][j]) + 128
    return C


def iDCT(D):
    """
    Perform The Inverce Discrete Cosign Transform
    on a given square matrix.

    The result is that of the following equation:
    N = round(T'DT) + 128

    :param D: The matrix result from a previous DCT.

    :returns: The matrix after Inverse DCT.
    """
    # TODO: Make sure this clips properly!
    # If length of D is 8, use the
    # pre-generated matrices.
    if len(D) == 8:
        global DCT_T8
        global DCT_Tp8
        T = DCT_T8
        TT = DCT_Tp8
    else:
        T = generate_DCT_matrix(len(D))
        TT = Matrix.transpose(T)
    # D is the matrix after de-quantization.
    A = Matrix.multiply(TT, D)
    return multiply_and_adjust(A, T)


# vim:ts=4:sts=4:sw=4:ai:et
