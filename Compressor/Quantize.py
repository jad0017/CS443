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


def scale_adjust(B, fact):
    """
    Scale a base matrix by a quality factor.
    Results are clipped to the range [0, 256).

    Equation:
        A(i,j) = round(B(i,j) * fact)

    :param B: Base matrix to scale.

    :returns: A scaled quantization matrix.
    """
    A = Matrix.zero_matrix(len(B[0]), len(B))
    for i in range(len(B)):
        for j in range(len(B[0])):
            A[i][j] = round(B[i][j] * fact)
            if A[i][j] > 255:
                A[i][j] = 255
    return A


def clip_matrix(M):
    """
    Clips a given matrix to the range [0, 256).

    :param M: Matrix to clip.

    :returns: A clipped matrix in the range [0, 256).
    """
    A = Matrix.zero_matrix(len(M[0]), len(M))
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] > 255:
                A[i][j] = 255
    return A


def quantize_scale_mat(B, qual=100):
    """
    Scale a base matrix by a quality factor.
    The resultant quantization matrix is based
    on the following piecewise definition:

             { clip( round( B(i,j) * fact ) )  if fact != 0
    Q(i,j) = {
             { B(i, j)                         if fact == 0

    :param B: Base matrix to scale based on given quality.
    :param qual: Desired quality scale; range: [0, 100]. (default: 100)

    :returns: A scaled quantization matrix.
    """
    if qual >= 50:
        fact = float(100 - qual) / 50.0
    else:
        fact = 50.0 / float(qual)
    if fact != 0:
        return scale_adjust(B, fact)
    # I don't think clipping here is necessary... not sure though
    return clip_matrix(B)


def quantize(D, B, qual=100):
    """
    Quantize a given matrix.
    Based on the following equation:

    C(i,j) = round( D(i,j) / Q(i,j) )

    Where Q is the scaled base matrix, :param B:.

    :param D:
        The result of DCT. (Matrix to quantize)
    :param B:
        The quantization base matrix.
    :param qual:
        The quality to scale the quantization by;
        range: [0,100] (default: 100).

    :returns: A quantized matrix.
    """
    Q = quantize_scale_mat(B, qual)
    C = Matrix.zero_matrix(len(D[0]), len(D))
    for i in range(len(D)):
        for j in range(len(D[0])):
            C[i][j] = round( D[i][j] / Q[i][j] )
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
            C[i][j] = A[i][j] * B[i][j]
    return C


def dequantize(C, B, qual=100):
    """
    Dequantize a given matrix.
    Calculates the following equation:

    D(i,j) = Q(i,j) * C(i,j)

    Where Q is the scaled base-quantization
    matrix, :param B:.

    :param C:
        Matrix to dequantize.
    :param B:
        Base quantization matrix.
    :param qual:
        The quality to scale the quantization matrix by;
        range: [0, 100] (default: 100).

    :returns: A dequantized matrix.
    """
    Q = quantize_scale_mat(B, qual)
    return multiply_each(Q, C)


# vim:ts=4:sw=4:sts=4:ai:et
