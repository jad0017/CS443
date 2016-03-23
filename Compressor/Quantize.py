import math
# Local imports
import Matrix

# Base quantization matrices given in the slides.

QBASE_LUM = [
    [  16,  11,  10,  16,  24,  40,  51,  61 ],
    [  12,  12,  14,  19,  26,  58,  60,  55 ],
    [  14,  13,  16,  24,  40,  57,  69,  56 ],
    [  14,  17,  22,  29,  51,  87,  80,  62 ],
    [  18,  22,  37,  56,  68, 109, 113,  77 ],
    [  24,  35,  55,  64,  81, 104, 113,  92 ],
    [  49,  64,  78,  87, 103, 121, 120, 101 ],
    [  72,  92,  95,  98, 112, 100, 103,  99 ],
]

QBASE_CHR = [
    [  17,  18,  24,  47,  99,  99,  99,  99 ],
    [  18,  21,  26,  66,  99,  99,  99,  99 ],
    [  24,  26,  56,  99,  99,  99,  99,  99 ],
    [  47,  66,  99,  99,  99,  99,  99,  99 ],
    [  99,  99,  99,  99,  99,  99,  99,  99 ],
    [  99,  99,  99,  99,  99,  99,  99,  99 ],
    [  99,  99,  99,  99,  99,  99,  99,  99 ],
    [  99,  99,  99,  99,  99,  99,  99,  99 ],
]


def quantize(D, Q):
    """
    Quantize a given matrix.
    Based on the following equation:

    C(i,j) = round( D(i,j) / Q(i,j) )

    :param D:
        The result of DCT. (Matrix to quantize)
    :param Q:
        The quantization base matrix.

    :returns: A quantized matrix.
    """
    C = Matrix.zero_matrix(len(D[0]), len(D))
    for i in range(len(D)):
        for j in range(len(D[0])):
            #C[i][j] = round( D[i][j] / Q[i][j] )
            C[i][j] = int(round( D[i][j] / Q[i][j] ) + 128)
    return C


def multiply_each(A, B):
    """
    Performs element-wise multiplication
    on two martrices of identical dimensions.
    Calculates the following equation:

    C(i,j) = A(i,j) * B(i,j)

    :param A: Matrix 1.
    :param B: Matrix 2.

    :returns: The result of element-wise
    matrix multiplication.
    """
    C = Matrix.zero_matrix(len(A[0]), len(A))
    for i in range(len(A)):
        for j in range(len(A[0])):
            #C[i][j] = A[i][j] * B[i][j]
            C[i][j] = A[i][j] * ( B[i][j] - 128 )
    return C


def dequantize(C, Q):
    """
    Dequantize a given matrix.
    Calculates the following equation:

    D(i,j) = Q(i,j) * C(i,j)

    :param C:
        Matrix to dequantize.
    :param Q:
        Base quantization matrix.

    :returns: A dequantized matrix.
    """
    return multiply_each(Q, C)


# vim:ts=4:sw=4:sts=4:ai:et
