# The PIL python library is required to run this script.
from PIL import Image

import sys
import math
import Compressor.Colors

def usage():
    print("Usage: %s file1.jpg file2.jpg" % (sys.argv[0],))
    sys.exit(1)


def error_gray(im1, im2):
    s = 0

    for Y in range(im1.size[1]):
        for X in range(im1.size[0]):
            s1 = im1.getpixel((X, Y))
            s2 = im2.getpixel((X, Y))

            s += pow(s1 - s2, 2)
    scalar = (im1.size[0] * im2.size[1])

    s /= scalar
    print("MSE:", str(s))

    # PSNR

    if s != 0:
        s = 20 * math.log10(255 / math.sqrt(s))
    print("PSNR:", str(s))



def error_rgb(im1, im2):
    (rs,  gs,  bs) = (0, 0, 0)
    (ys, cbs, crs) = (0, 0, 0)

    for Y in range(im1.size[1]):
        for X in range(im1.size[0]):
            (r1, g1, b1) = im1.getpixel((X, Y))
            (r2, g2, b2) = im2.getpixel((X, Y))

            rs += pow(r1 - r2, 2)
            gs += pow(g1 - g2, 2)
            bs += pow(b1 - b2, 2)

            (y1, cb1, cr1) = Compressor.Colors.RGB_to_YCbCr_single(r1, g1, b1)
            (y2, cb2, cr2) = Compressor.Colors.RGB_to_YCbCr_single(r2, g2, b2)

            ys  += pow( y1 -  y2, 2)
            cbs += pow(cb1 - cb2, 2)
            crs += pow(cr1 - cr2, 2)

    scalar = (im1.size[0] * im2.size[1])

    rs /= scalar
    gs /= scalar
    bs /= scalar

    ys  /= scalar
    cbs /= scalar
    crs /= scalar

    print("MSE:")
    print(" R:", str(rs), "   G:", str(gs), "   B:", str(bs))
    print(" Y:", str(ys), "  Cb:", str(cbs), "  Cr:", str(crs))

    # PSNR

    if rs != 0:
        rs = 20 * math.log10(255 / math.sqrt(rs))
    if gs != 0:
        gs = 20 * math.log10(255 / math.sqrt(gs))
    if bs != 0:
        bs = 20 * math.log10(255 / math.sqrt(bs))

    if ys != 0:
        ys = 20 * math.log10(255 / math.sqrt(ys))
    if cbs != 0:
        cbs = 20 * math.log10(255 / math.sqrt(cbs))
    if crs != 0:
        crs = 20 * math.log10(255 / math.sqrt(crs))

    print("PSNR:")
    print(" R:", str(rs), "   G:", str(gs), "   B:", str(bs))
    print(" Y:", str(ys), "  Cb:", str(cbs), "  Cr:", str(crs))


if not len(sys.argv) is 3:
    usage()
    sys.exit(1)

im1 = Image.open(sys.argv[1])
im2 = Image.open(sys.argv[2])

if im1.mode != im2.mode:
    print("Image modes differ!")
    sys.exit(1)

if im1.size != im2.size:
    print("Images are different sizes!")
    sys.exit(1)

if im1.mode == 'L':
    error_gray(im1, im2)
elif im1.mode == 'RGB':
    error_rgb(im1, im2)
else:
    print("Unsupported Color Mode:", im1.mode)
    sys.exit(1)
sys.exit(0)

# vim:ts=4:sws=4:st=4:ai
