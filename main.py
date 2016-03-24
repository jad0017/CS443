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
import Compressor.DCT
import Compressor.NCage
import Compressor.Matrix
import Compressor.Quantize
import Compressor.RLC

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


def get_block(pixels, xbp, ybp, N, block_type):
    (xoff, xlen) = xbp
    (yoff, ylen) = ybp
    M = Compressor.Matrix.zero_matrix(N, btype=block_type)
    for yo in range(ylen):
        y = yoff + yo
        for xo in range(xlen):
            M[yo][xo] = pixels[xoff + xo, y]
    return M


def compress_image(img, oimg, compress_block_fn, block_type):
    N = 8
    (width, height) = img.size

    width_mod = width % N
    width_blocks = width // N
    width_bp = (width - width_mod, width_mod)

    height_mod = height % N
    height_blocks = height // N
    height_bp = (height - height_mod, height_mod)

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
        yoff = yb * N
        ybp = (yoff, N)
        for xb in range(width_blocks):
            M = get_block(pixels, (xb * N, N), ybp, N, block_type)
            compress_block_fn(oimg, M)
        # Address partial width block
        if width_mod != 0:
            M = get_block(pixels, width_bp, ybp, N, block_type)
            compress_block_fn(oimg, M)
    # Address parital height block
    if height_mod != 0:
        for xb in range(width_blocks):
            M = get_block(pixels, (xb * N, N), height_bp, N, block_type)
            compress_block_fn(oimg, M)
        # Address lower right block if partial height and partial width
        if width_mod != 0:
            M = get_block(pixels, width_bp, height_bp, N, block_type)
            compress_block_fn(oimg, M)
    return True



def compress_grayscale_block(oimg, M):
    # Single Channel: Luminance
    D = Compressor.DCT.DCT(M)
    #print(str(D))
    C = Compressor.Quantize.quantize(D, Compressor.Quantize.QBASE_LUM)
    #print(str(C))
    R = Compressor.RLC.RLC(C)
    #print(str(R))
    oimg.write_block_rlc(R)


def decompress_grayscale_block(R):
    C = Compressor.RLC.iRLC(R, 8)
    D = Compressor.Quantize.dequantize(C, Compressor.Quantize.QBASE_LUM)
    M = Compressor.DCT.iDCT(D)
    return M


def compress_grayscale_image(img, oimg):
    return compress_image(img, oimg, compress_grayscale_block, 0)


def copy_block(img, M, xbp, ybp, N):
    # TODO: Investigate putdata(data, scale, offset)
    # data is a list:
    # pixel = <idx> * scale + offset
    # Sooo img.putdata(M[y][0:xlen], xoff, yoff * N)?
    (xoff, xlen) = xbp
    (yoff, ylen) = ybp
    for yo in range(ylen):
        y = yoff + yo
        for xo in range(xlen):
            img.putpixel((xoff + xo, y), M[yo][xo])


def decompress_grayscale_image(img, outfile):
    N = 8
    (width, height) = img.size
    (wblocks, hblocks) = img.size_blocks
    (twblocks, thblocks) = img.size_true_blocks

    width_mod = width % N
    width_bp = (width - width_mod, width_mod)

    height_mod = height % N
    height_bp = (height - height_mod, height_mod)

    oimg = Image.new('L', img.size)

    # Should probably check len(img) at some point
    # but the exception handler will cover us.
    blkidx = 0
    for yb in range(hblocks):
        ybp = (yb * N, N)
        for xb in range(wblocks):
            R = img[blkidx]
            blkidx += 1
            M = decompress_grayscale_block(R)
            copy_block(oimg, M, (xb * N, N), ybp, N)
        if twblocks != wblocks:
            # We have a partial X block to take care off
            R = img[blkidx]
            blkidx += 1
            M = decompress_grayscale_block(R)
            copy_block(oimg, M, width_bp, ybp, N)
    if thblocks != hblocks:
        # Partial Y block
        for xb in range(wblocks):
            R = img[blkidx]
            blkidx += 1
            M = decompress_grayscale_block(R)
            copy_block(oimg, M, (xb * N, N), height_bp, N)
        # Partial Y and Partial X block (bottom right corner)
        if twblocks != wblocks:
            R = img[blkidx]
            blkidx += 1
            M = decompress_grayscale_block(R)
            copy_block(oimg, M, width_bp, height_bp, N)
    # They're getting a BMP.  Don't care if they don't want it.
    oimg.save(outfile, 'BMP')


def compress_rgb_blocks(oimg, M):
    # Each block holds pixel tuples: (R, G, B)
    # First convert to YCbCr
    # Then DCT each channel
    # Then Quantize each channel
    # Then RLC each channel
    # Then write each channel to the file (Y -> Cb -> Cr)
    print("Unsupported!")
    sys.exit(1)


def decompress_rgb_block(R, quant):
    # Need to know the quantization type since this is a single block
    # not all three.
    # First iRLC(R, 8)
    # Then Dequantize(C, quant)
    # Then iDCT(D)
    # Finally return the matrix
    print("Unsupported!")
    sys.exit(1)


def compress_rgb_image(img, oimg):
    return compress_image(img, oimg, compress_rgb_block, (0, 0, 0))


def decompress_rgb_image(img, outfile):
    print("Unsupported!")
    sys.exit(1)


if len(sys.argv) != 4:
    print("Usage: {} <c|d> <input> <output.ncage>".format(sys.argv[0]))
    sys.exit(1)

op = sys.argv[1]
infile = sys.argv[2]
outfile = sys.argv[3]

if op == 'c':
    img = Image.open(infile)
    mode = test_image_mode(img)
    oimg = Compressor.NCage.NCageWriter(outfile, img.size[0], img.size[1], mode)

    if mode == Compressor.NCage.MODE_GRAYSCALE:
        compress_grayscale_image(img, oimg)
    else: # Only other mode is MODE_RGB
        compress_rgb_image(img, oimg)
    oimg.close()
elif op == 'd':
    img = Compressor.NCage.NCageReader()
    img.load(infile)

    if img.mode == Compressor.NCage.MODE_GRAYSCALE:
        decompress_grayscale_image(img, outfile)
    else: # Only other mode is MODE_RGB
        decompress_rgb_image(img, outfile)
else:
    print("Unknown operation: ", op)
    sys.exit(1)

sys.exit(0)
