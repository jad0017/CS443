from . import Matrix

def YCbCr_to_RGB_single(y, cb, cr):
    crt = cr - 128
    cbt = cb - 128

    r = int(y + (1.402 * crt))
    g = int(y - (0.34414 * cbt) - (0.71414 * crt))
    b = int(y + (1.772 * cbt))

    return (r, g, b)


def YCbCr_to_RGB(M):
    A = Matrix.zero_matrix(len(M[0]), len(M))

    for Y in range(len(M)):
        for X in range(len(M[0])):
            (y, cb, cr) = M[Y][X]
            A[Y][X] = YCbCr_to_RGB_single(y, cb, cr)
    return A


def RGB_to_YCbCr_single(r, g, b):
    y  = min(int((0.299 * r) + (0.587 * g) + (0.144 * b)), 255)
    cb = min(int((-0.168736 * r) + (-0.331264 * g) + (0.5 * b) + 128), 255)
    cr = min(int((0.5 * r) + (-0.418688 * g) + (-0.081312 * b) + 128), 255)

    return (y, cb, cr)


def RGB_to_YCbCr(M):
    A = Matrix.zero_matrix(len(M[0]), len(M))

    for Y in range(len(M)):
        for X in range(len(M[0])):
            (r, g, b) = M[Y][X]
            A[Y][X] = RGB_to_YCbCr_single(r, g, b)
    return A


# vim:ts=4:sws=4:st=4:autoindent
