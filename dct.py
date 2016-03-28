import sys
import pickle

def usage():
    print("Usage: %s file.dct wblock hblock\n" % (sys.argv[0],))
    print("Block Maximas are computed as follows:")
    print("  wblocks = (width // 8) + int((width % 8) != 0)")
    print("  hblocks = (height // 8) + int((height % 8) != 0)\n")
    sys.exit(1)


if len(sys.argv) != 4:
    usage()
    sys.exit(1)

infile = open(sys.argv[1], 'rb')

try:
    wblock = int(sys.argv[2])
    hblock = int(sys.argv[3])
except:
    print("Invalid block format!")
    usage()
    sys.exit(1)

try:
    (width, height) = pickle.load(infile)
except:
    print("Invalid DCT file!")
    sys.exit(1)

wblocks = (width // 8) + int((width % 8) != 0)
hblocks = (height // 8) + int((height % 8) != 0)

if (wblock >= wblocks) or (wblock < 0):
    print("wblock out of range!")
    sys.exit(1)

if (hblock >= hblocks) or (hblock < 0):
    print("hblock out of range!")
    sys.exit(1)

block_number = (hblock * wblocks) + wblock

for i in range(block_number + 1):
    M = pickle.load(infile)

print("Block %d (%d, %d):" % (block_number, wblock, hblock))
for y in range(len(M)):
    sys.stdout.write("[ ")
    for x in range(len(M[0])):
        sys.stdout.write("{} ".format(M[y][x]))
    sys.stdout.write("]\n")
    sys.stdout.flush()

sys.exit(0)

# vim:ts=4:sws=4:st=4:ai
