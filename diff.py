# The PIL python library is required to run this script.
from PIL import Image

import sys
import math
import Compressor.Colors

def usage():
    print("Usage: %s file1.jpg file2.jpg output.bmp" % (sys.argv[0],))
    sys.exit(1)


def val(p1, p2):
    if p1 > p2:
        return 255 - (p1 - p2)
    return p2 - p1


def diff_gray(im1, im2, outfile):
    oimg = Image.new('L', im1.size)
    for Y in range(im1.size[1]):
        for X in range(im1.size[0]):
            p1 = im1.getpixel((X, Y))
            p2 = im2.getpixel((X, Y))
            oimg.putpixel((X,Y), val(p1, p2))
    oimg.save(outfile, 'BMP')


def diff_rgb(im1, im2, outfile):
    oimg = Image.new('RGB', im1.size)
    for Y in range(im1.size[1]):
        for X in range(im1.size[0]):
            (r1, g1, b1) = im1.getpixel((X, Y))
            (r2, g2, b2) = im2.getpixel((X, Y))
            P = (val(r1, r2), val(g1, g2), val(b1, b2))
            oimg.putpixel((X,Y), P)
    oimg.save(outfile, 'BMP')


if len(sys.argv) != 4:
    usage()
    sys.exit(1)

im1 = Image.open(sys.argv[1])
im2 = Image.open(sys.argv[2])
outfile = sys.argv[3]

if im1.mode != im2.mode:
    print("Image modes differ!")
    sys.exit(1)

if im1.size != im2.size:
    print("Images are different sizes!")
    sys.exit(1)

if im1.mode == 'L':
    diff_gray(im1, im2, outfile)
elif im1.mode == 'RGB':
    diff_rgb(im1, im2, outfile)
else:
    print("Unsupported Color Mode:", im1.mode)
    sys.exit(1)
sys.exit(0)

# vim:ts=4:sws=4:st=4:ai
