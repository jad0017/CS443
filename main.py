# This is from the PIL module.
# I recommend using the pillow fork instead (same import name/module).
#
# Linux and OSX:
#   easy_install pillow   (or PIL if you're feeling lucky)
#
# Windows:
#   Wish upon a star?
#
from PIL import Image

import sys
import Compressor

def test_image_mode(img):
    mode = img.mode
    if mode == '1':
        print("Unsupported Image Mode: 1-bit(black and white)")
        sys.exit(1)
    elif mode == 'L':
        return Compressor.NCage.MODE_GRAYSCALE
    elif mode == 'RGB':
        return Compressor.NCage.MODE_RGB
    elif mode == 'RGBA':
        print("Unsupported Image Mode: RGBA")
        sys.exit(1)
    elif mode == 'P':
        print("Unsupported Image Mode: Palette")
        sys.exit(1)
    print("Unsupported Image Mode:", mode)
    sys.exit(1)


def get_block(img, pixels, xb, yb, N):
    x_off = N * xb
    y_off = N * yb
    M = Compressor.Matrix.zero_square_matrix(N)
    for y in range(y_off, y_off + N):
        ymod = y % N
        for x in range(x_off, x_off + N):
            M[ymod][x % N] = pixels[x, y])
    return M


def get_block_partial_width(img, pixels, x_off, yb, N):
    (width, height) = img.size
    xlen = width - x_off
    xolen = N - xlen
    y_off = N * yb
    M = Compressor.Matrix.zero_square_matrix(N)
    for y in range(y_off, y_off + N):
        ymod = y % N
        for xo in range(xlen):
            M[ymod][xo] = pixels[x_off + xo, y]
        for xo in range(xolen):
            M[ymod][xlen + xo] = 0
    return M


def get_block_partial_height(img, pixels, xb, y_off, N):
    (width, height) = img.size
    ylen = height - y_off
    yolen = N - ylen
    x_off = N * xb
    M = Compressor.Matrix.zero_square_matrix(N)
    for yo in range(ylen):
        for x in range(x_off, x_off + N):
            M[yo][x % N] = pixels[x, y_off + yo]
    for yo in range(yolen):
        for x in range(N):
            M[ylen + yo][x] = 0
    return M


def get_block_bottom_right(img, pixels, x_off, y_off, N):
    (width, height) = img.size
    xlen = width - x_off
    xolen = N - xlen
    ylen = height - y_off
    yolen = N - ylen
    M = Compressor.Matrix.zero_square_matrix(N)
    for yo in range(ylen):
        for xo in range(xlen):
            M[yo][x % N] = pixels[x_off + xo, y_off + yo]
        for xo in range(xolen):
            M[yo][xlen + xo] = 0
    for yo in range(yolen):
        for x in range(N):
            M[ylen + yo][x] = 0
    return M


def compress_grayscale_block(oimg, M):
    # Single Channel: Luminance
    D = Compressor.DCT.DCT(M)
    C = Compressor.Quantize.quantize(D, Compressor.Quantize.QBASE_LUM)
    R = Compressor.RLC.RLC(C)
    oimg.write_block_rlc(R)


def decompress_grayscale_block(R):
    C = Compressor.RLC.iRLC(R, 8)
    D = Compressor.Quantize.dequantize(C, Compressor.Quantize.QBASE_LUM)
    M = Compressor.DCT.iDCT(D)
    return M


def compress_grayscale_image(img, oimg):
    (width, height) = img.size

    width_off = 8 - (width % 8)
    if width_off == 8:
        width_off = 0
    width_off_pos = width - (width % 8)
    width_blocks = width // 8

    height_off = 8 - (height % 8)
    if height_off == 8:
        height_off = 0
    height_off_pos = height - (height % 8)
    height_blocks = height // 8

    #
    # The gist of this:
    #
    #  Loop over y blocks:
    #    Loop over x blocks.
    #    Loop over x overflow block.
    #  Loop over y overflow block:
    #    Loop over x blocks.
    #    Loop over x overflow block.
    #
    # This is probably the ugliest thing I've written in a long time.
    #

    pixels = img.load()
    for yb in range(height_blocks):
        for xb in range(width_blocks):
            #print("Block(%d, %d):" % (xb, yb))
            M = get_block(img, pixels, xb, yb, N)
            compress_grayscale_block(oimg, M)
        # Address partial width block
        if width_off != 0:
            #print("Block(%d, %d):" % (width_blocks, yb))
            M = get_block_partial_width(img, pixels, width_off_pos, yb, N)
            compress_grayscale_block(oimg, M)
    if height_off != 0:
        for xb in range(width_blocks):
            #print("Block(%d, %d):" % (xb, height_blocks))
            M = get_block_partial_height(img, pixels, xb, height_off_pos, N)
            compress_grayscale_block(oimg, M)
        if width_off != 0:
            #print("Block(%d, %d):" % (width_blocks, height_blocks))
            M = get_block_bottom_right(img, pixels, width_off_pos, height_off_pos, N)
            compress_grayscale_block(oimg, M)
    return True



def compress_rgb_image(img, oimg):
    print "Unsupported"


if len(sys.argv) != 3:
    print("Usage: {} <input> <output.ncage>".format(sys.argv[0]))
    sys.exit(1)

infile = sys.argv[1]
outfile = sys.argv[2]

img = Image.open(infile)
mode = test_image_mode(img)
oimg = Compressor.NCage.NCageWriter(outfile, img.size[0], img.size[1], mode)

if mode == Compressor.NCage.MODE_GRAYSCALE:
    compress_grayscale_image(img, oimg)
else: # Only other mode is MODE_RGB
    compress_rgb_image(img, oimg)

oimg.close()

sys.exit(0)
