import sys
import getopt
import pickle

def die_usage(ret=1):
    print("Usage: %s [--print-size] file.dct" % sys.argv[0])
    print("       %s --by-block file.dct wblock hblock" % sys.argv[0])
    print("       %s --by-pixel file.dct X Y" % sys.argv[0])
    print("       %s --by-block-num file.dct block\n" % sys.argv[0])
    print("Options:")
    print("  -b, --by-block      Reference DCT block by width and height")
    print("                      block position.")
    print("  -B, --by-block-num  Reference DCT block by a single block")
    print("                      number.")
    print("  -P, --print-size    Print various sizes (useful stuff).")
    print("                      [Default]")
    print("  -p, --by-pixel      Reference DCT block containing a pixel")
    print("                      defined by an (X,Y) pair.")
    sys.exit(ret)


print_size = 0
by_block = 0
by_pixel = 0
by_block_num = 0

def validate_type():
    global print_size
    global by_block
    global by_pixel
    global by_block_num
    x = print_size + by_block + by_pixel + by_block_num
    if x > 1:
        print("Only one of --print-size, --by-block, --by-pixel, and",
              "--by-block-num may be specified!")
        sys.exit(1)
    return True


def check_nargs(name, count, nargs):
    if nargs < count:
        print("Missing arguments for %s!" % name)
        die_usage()
    if nargs > count:
        print("Too many arguments for %s!" % name)
        die_usage()
    return True


def get_dims(fd):
    try:
        (width, height) = pickle.load(fd)
    except:
        print("Invalid DCT file!")
        sys.exit(1)
    return (width, height)


def cast_uint(s):
    try:
        ret = int(s)
    except ValueError:
        print("%s is not a valid integer!")
        sys.exit(1)
    if ret < 0:
        print("%s is not a positive integer!")
        sys.exit(1)
    return ret


def calc_blocks(width, height):
    wblocks = (width // 8) + int((width % 8) != 0)
    hblocks = (height // 8) + int((height % 8) != 0)
    nblocks = wblocks * hblocks
    return (wblocks, hblocks, nblocks)


def print_block(M):
    for y in range(len(M)):
        sys.stdout.write("[ ")
        for x in range(len(M[0])):
            sys.stdout.write("{} ".format(M[y][x]))
        sys.stdout.write("]\n")
        sys.stdout.flush()


def get_block(N, fd):
    for i in range(N + 1):
        M = pickle.load(fd)
    return M


try:
    longopts=["help","print-size","by-block","by-pixel","by-block-num"]
    opts, args = getopt.getopt(sys.argv[1:], "hbBpP", longopts)
except getopt.GetoptError as err:
    print(str(err))
    die_usage()

for o,a in opts:
    if o in ("-h", "--help"):
        die_usage(0)
    elif o in ("-b", "--by-block"):
        by_block = 1
        validate_type()
    elif o in ("-B", "--by-block-num"):
        by_block_num = 1
        validate_type()
    elif o in ("-p", "--by-pixel"):
        by_pixel = 1
        validate_type()
    elif o in ("-P", "--print-size"):
        print_size = 1
        validate_type()
    else:
        print("Unknown option:", o)
        die_usage()

x = print_size + by_block + by_pixel + by_block_num
if x == 0:
    print_size = 1



if print_size != 0:
    check_nargs("--print-size", 1, len(args))
    infile = open(args[0], 'rb')
    (width, height) = get_dims(infile)
    infile.close()
    (wblocks, hblocks, nblocks) = calc_blocks(width, height)
    print("Dimensions of %s:" % args[0])
    print("  Width:   %d,  Height:  %d" % (width, height))
    print("  WBlocks: %d,  HBlocks: %d" % (wblocks, hblocks))
    print("  Total Blocks: %d" % nblocks)
    sys.exit(0)

if by_block_num != 0:
    check_nargs("--by-block-num", 2, len(args))
    infile = open(args[0], 'rb')
    (width, height) = get_dims(infile)
    (wblocks, hblocks, nblocks) = calc_blocks(width, height)
    block = cast_uint(args[1])
    if block >= nblocks:
        print("%d is too large! Maximum block: %d" % (block, nblocks - 1))
        sys.exit(1)
    print("Block %d:" % block)
    M = get_block(block, infile)
    infile.close()
    print_block(M)
    sys.exit(0)


if by_block != 0:
    check_nargs("--by-block", 3, len(args))
    infile = open(args[0], 'rb')
    (width, height) = get_dims(infile)
    (wblocks, hblocks, nblocks) = calc_blocks(width, height)
    wblock = cast_uint(args[1])
    hblock = cast_uint(args[2])
    if wblock >= wblocks:
        print("%d is too large! Maximum wblock: %d" % (wblock, wblocks - 1))
        sys.exit(1)
    if hblock >= hblocks:
        print("%d is too large! Maximum hblock: %d" % (hblock, hblocks - 1))
        sys.exit(1)
    block = (hblock * wblocks) + wblock
    print("Block %d (%d, %d):" % (block, wblock, hblock))
    M = get_block(block, infile)
    infile.close()
    print_block(M)
    sys.exit(0)


if by_pixel != 0:
    check_nargs("--by-block", 3, len(args))
    infile = open(args[0], 'rb')
    (width, height) = get_dims(infile)
    (wblocks, hblocks, nblocks) = calc_blocks(width, height)
    X = cast_uint(args[1])
    Y = cast_uint(args[2])
    wblock = (X // 8) + int((X % 8) != 0)
    hblock = (Y // 8) + int((Y % 8) != 0)
    if X >= width:
        print("%d is too large! Width: %d" % (X, width))
        sys.exit(1)
    if Y >= height:
        print("%d is too large! Height: %d" % (Y, height))
        sys.exit(1)
    block = (hblock * wblocks) + wblock
    print("Block %d (%d, %d) containing (%d, %d):"
           % (block, wblock, hblock, X, Y))
    M = get_block(block, infile)
    infile.close()
    print_block(M)

sys.exit(0)

# vim:ts=4:sws=4:st=4:ai
