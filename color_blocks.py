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
import Compressor.Matrix


def to_rgb(M):
    print("Missing codes!")
    sys.exit(1)


def to_ycbcr(M):
    print("Missing codes!")
    sys.exit(1)


def test_image_mode(img):
    mode = img.mode
    if mode == '1':
        print("Unsupported Image Mode: 1-bit(black and white)")
        sys.exit(1)
    elif mode == 'L':
        print("Unsupported Image Mode: Grayscale")
        sys.exit(1)
    elif mode == 'RGB':
        return True
    elif mode == 'RGBA':
        print("Unsupported Image Mode: RGBA")
        sys.exit(1)
    elif mode == 'P':
        print("Unsupported Image Mode: Palette")
        sys.exit(1)
    print("Unsupported Image Mode:", mode)
    sys.exit(1)


def get_block(pixels, xbp, ybp, N, block_type):
    (xoff, xlen) = xbp
    (yoff, ylen) = ybp
    M = Compressor.Matrix.zero_matrix(N, btype=block_type)
    for yo in range(ylen):
        y = yoff + yo
        for xo in range(xlen):
            M[yo][xo] = pixels[xoff + xo, y]
    return M


def copy_block(img, M, xbp, ybp, N):
    (xoff, xlen) = xbp
    (yoff, ylen) = ybp
    for yo in range(ylen):
        y = yoff + yo
        for xo in range(xlen):
            img.putpixel((xoff + xo, y), M[yo][xo])


def do_stuff(img, oimg, convertion_fn):
    N = 8
    (width, height) = img.size
    block_type=(0,0,0)

    width_mod = width % N
    width_blocks = width // N
    width_bp = (width - width_mod, width_mod)

    height_mod = height % N
    height_blocks = height // N
    height_bp = (height - height_mod, height_mod)

    pixels = img.load()
    for yb in range(height_blocks):
        yoff = yb * N
        ybp = (yoff, N)
        for xb in range(width_blocks):
            M = get_block(pixels, (xb * N, N), ybp, N, block_type)
            M2 = convertion_fn(M)
            copy_block(oimg, M2, (xb * N, N), ybp, N)
        # Address partial width block
        if width_mod != 0:
            M = get_block(pixels, width_bp, ybp, N, block_type)
            M2 = convertion_fn(M)
            copy_block(oimg, M2, width_bp, ybp, N)
    # Address parital height block
    if height_mod != 0:
        for xb in range(width_blocks):
            M = get_block(pixels, (xb * N, N), height_bp, N, block_type)
            M2 = convertion_fn(M)
            copy_block(oimg, M2, (xb * N, N), height_bp, N)
        # Address lower right block if partial height and partial width
        if width_mod != 0:
            M = get_block(pixels, width_bp, height_bp, N, block_type)
            M2 = convertion_fn(M)
            copy_block(oimg, M2, width_bp, heightbp, N)
    return True


if len(sys.argv) != 4:
    print("Usage: {} <--to-rgb|--to-ycbcr> <input> <output.ncage>".format(sys.argv[0]))
    sys.exit(1)

op = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]

if op == '--to-rgb':
    img = Image.open(infile)
    test_image_mode(img)
    oimg = Image.new('RGB', img.size)
    do_stuff(img, oimg, to_rgb)
    oimg.save(outfile)
elif op == '--to-ycbcr':
    img = Image.open(infile)
    test_image_mode(img)
    oimg = Image.new('RGB', img.size)
    do_stuff(img,oimg, to_ycbcr)
    oimg.save(outfile)
else:
    print("Unknown operation: ", op)
    sys.exit(1)

sys.exit(0)
