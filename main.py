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
import getopt
from Compressor import Chroma
from Compressor import Colors
from Compressor import DCT
from Compressor import NCage
from Compressor import Matrix
from Compressor import Quantize
from Compressor import RLC

def usage():
    print("Usage: %s --compress [options] <input> <output.ncage>"
          % (sys.argv[0],))
    print("       %s --decompress [options] <input.ncage> <output.bmp>"
          % (sys.argv[0],))
    print("\nOptions:")
    print(" --chroma-subsampling=<spec>   Use Chroma Subsampling (ex. 4:2:0)")
    print(" --dump-dct-coefficients=<out> Dump DCT coefficients per block to")
    print("                               the file <out>.")


def test_image_mode(img):
    mode = img.mode
    if mode == '1':
        print("Unsupported Image Mode: 1-bit(black and white)")
        sys.exit(1)
    elif mode == 'L':
        return NCage.MODE_GRAYSCALE
    elif mode == 'RGB':
        return NCage.MODE_RGB
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
    M = Matrix.zero_matrix(N, btype=block_type)
    for yo in range(ylen):
        y = yoff + yo
        for xo in range(xlen):
            M[yo][xo] = pixels[xoff + xo, y]
    return M


def compress_image(img, oimg, compress_block_fn, block_type, spec):
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
            compress_block_fn(oimg, M, spec)
        # Address partial width block
        if width_mod != 0:
            M = get_block(pixels, width_bp, ybp, N, block_type)
            compress_block_fn(oimg, M, spec)
    # Address parital height block
    if height_mod != 0:
        for xb in range(width_blocks):
            M = get_block(pixels, (xb * N, N), height_bp, N, block_type)
            compress_block_fn(oimg, M, spec)
        # Address lower right block if partial height and partial width
        if width_mod != 0:
            M = get_block(pixels, width_bp, height_bp, N, block_type)
            compress_block_fn(oimg, M, spec)
    return True



def compress_grayscale_block(oimg, M, spec):
    # Single Channel: Luminance
    D = DCT.DCT(M)
    C = Quantize.quantize(D, Quantize.QBASE_LUM)
    R = RLC.RLC(C)
    oimg.write_block_rlc(R)


def decompress_grayscale_block(R):
    C = RLC.iRLC(R, 8)
    D = Quantize.dequantize(C, Quantize.QBASE_LUM)
    M = DCT.iDCT(D)
    return M


def compress_grayscale_image(img, oimg):
    return compress_image(img, oimg, compress_grayscale_block, 0, None)


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
    for yb in range(thblocks):
        ybp = (yb * N, N)
        for xb in range(twblocks):
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
        for xb in range(twblocks):
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


def compress_rgb_block(oimg, M, quant):
    D = DCT.DCT(M)
    C = Quantize.quantize(D, quant)
    R = RLC.RLC(C)
    oimg.write_block_rlc(R)


def compress_rgb_blocks(oimg, M, spec):
    # Each block holds pixel tuples: (R, G, B)
    # First convert to YCbCr
    # Then DCT each channel
    # Then Quantize each channel
    # Then RLC each channel
    # Then write each channel to the file (Y -> Cb -> Cr)
    A = Colors.RGB_to_YCbCr(M)

    # Split matrix into channels
    Y  = [[ A[y][x][0] for x in range(len(M[0]))] for y in range(len(M))]
    CB = [[ A[y][x][1] for x in range(len(M[0]))] for y in range(len(M))]
    CR = [[ A[y][x][2] for x in range(len(M[0]))] for y in range(len(M))]

    # Lumenance
    compress_rgb_block(oimg, Y, Quantize.QBASE_LUM)
    # Chromanance
    CB = Chroma.chroma_subsample(CB, spec)
    compress_rgb_block(oimg, CB, Quantize.QBASE_CHR)
    CR = Chroma.chroma_subsample(CR, spec)
    compress_rgb_block(oimg, CR, Quantize.QBASE_CHR)


def decompress_rgb_block(R, quant):
    # Need to know the quantization type since this is a single block
    # not all three.
    C = RLC.iRLC(R, 8)
    D = Quantize.dequantize(C, quant)
    M = DCT.iDCT(D)
    return M


def compress_rgb_image(img, oimg, spec):
    return compress_image(img, oimg, compress_rgb_blocks, (0, 0, 0), spec)


def get_dec_rgb_block(img, blk):
    R = img[blk]
    blk += 1
    Y = decompress_rgb_block(R, Quantize.QBASE_LUM)
    R = img[blk]
    blk += 1
    CB = decompress_rgb_block(R, Quantize.QBASE_CHR)
    R = img[blk]
    blk += 1
    CR = decompress_rgb_block(R, Quantize.QBASE_CHR)
    A = Matrix.zero_matrix(len(Y[0]), len(Y))
    for y in range(len(Y)):
        for x in range(len(Y[0])):
            A[y][x] = (Y[y][x], CB[y][x], CR[y][x])
    return Colors.YCbCr_to_RGB(A)


def decompress_rgb_image(img, outfile):
    N = 8
    (width, height) = img.size
    (wblocks, hblocks) = img.size_blocks
    (twblocks, thblocks) = img.size_true_blocks

    width_mod = width % N
    width_bp = (width - width_mod, width_mod)

    height_mod = height % N
    height_bp = (height - height_mod, height_mod)

    oimg = Image.new('RGB', img.size)

    # Should probably check len(img) at some point
    # but the exception handler will cover us.
    blkidx = 0
    for yb in range(thblocks):
        ybp = (yb * N, N)
        for xb in range(twblocks):
            M = get_dec_rgb_block(img, blkidx)
            blkidx += 3
            copy_block(oimg, M, (xb * N, N), ybp, N)
        if twblocks != wblocks:
            # We have a partial X block to take care off
            M = get_dec_rgb_block(img, blkidx)
            blkidx += 3
            copy_block(oimg, M, width_bp, ybp, N)
    if thblocks != hblocks:
        # Partial Y block
        for xb in range(twblocks):
            M = get_dec_rgb_block(img, blkidx)
            blkidx += 3
            copy_block(oimg, M, (xb * N, N), height_bp, N)
        # Partial Y and Partial X block (bottom right corner)
        if twblocks != wblocks:
            M = get_dec_rgb_block(img, blkidx)
            blkidx += 3
            copy_block(oimg, M, width_bp, height_bp, N)
    # They're getting a BMP.  Don't care if they don't want it.
    oimg.save(outfile, 'BMP')


try:
    longopts=["help","compress","decompress","dump-dct-coefficients=",
              "chroma-subsampling="]
    opts, args = getopt.getopt(sys.argv[1:], "hcd", longopts)
except getopt.GetoptError as err:
    print(str(err))
    usage()
    sys.exit(1)

dct_output = None
chroma_spec = "4:4:4"
infile = None
outfile = None

compress = False
decompress = False

for o,a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit(0)
    elif o in ("-c", "--compress"):
        if (compress == True) or (decompress == True):
            print("Only one of --compress and --decompress may be specified!")
            usage()
            sys.exit(1)
        compress = True
    elif o in ("-d", "--decompress"):
        if (compress == True) or (decompress == True):
            print("Only one of --compress and --decompress may be specified!")
            usage()
            sys.exit(1)
        decompress = True
    elif o == "--chroma-subsampling":
        chroma_spec = a
    elif o == "--dunp-dct-coefficients":
        dct_output = a
    else:
        print("Unknown option:", o)
        usage()
        sys.exit(1)

if len(args) < 2:
    print("Missing arguments!")
    usage()
    sys.exit(1)
elif len(args) > 2:
    print("Too many arguments!")
    usage()
    sys.exit(1)

infile = args[0]
outfile = args[1]

if compress:
    img = Image.open(infile)
    mode = test_image_mode(img)
    oimg = NCage.NCageWriter(outfile, img.size[0], img.size[1], mode)

    if mode == NCage.MODE_GRAYSCALE:
        compress_grayscale_image(img, oimg)
    else: # Only other mode is MODE_RGB
        compress_rgb_image(img, oimg, chroma_spec)
    oimg.close()
elif decompress:
    img = NCage.NCageReader()
    img.load(infile)

    if img.mode == NCage.MODE_GRAYSCALE:
        decompress_grayscale_image(img, outfile)
    else: # Only other mode is MODE_RGB
        decompress_rgb_image(img, outfile)
else:
    print("One of --compress and --decompress must be specified!")
    usage()
    sys.exit(1)

sys.exit(0)
