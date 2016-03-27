from . import Matrix

def YCbCr_to_RGB(M):
    A = Matrix.zero_matrix(len(M[0]), len(M))

    for y in range(len(M)):
        for x in range(len(M[0])):
            (y, cb, cr) = M[y][x]
            cr -= 128
            cb -= 128

            r = int(y + (1.402 * cr))
            g = int(y - (0.34414 * cb) - (0.71414 * cr))
            b = int(y + (1.772 * cb))

            A[y][x] = (r, g, b)
    return A


def RGB_to_YCbCr(M):
    A = Matrix.zero_matrix(len(M[0]), len(M))

    for y in range(len(M)):
        for x in range(len(M[0])):
            (r, g, b) = M[y][x]

            y  = int((0.299 * r) + (0.587 * g) + (0.144 * b))
            cb = int((-0.168736 * r) + (-0.331264 * g) + (0.5 * b) + 128)
            cr = int((0.5 * r) + (-0.418688 * g) + (-0.081312 * b) + 128)

            A[y][x] = (y, cb, cr)
    return A


# vim:ts=4:sws=4:st=4:autoindent
