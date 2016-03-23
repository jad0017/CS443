import struct

# Module for reading/writing NCage format files.
#
# Format:
#   5B magic (ascii 'NCAGE')
#   1B mode (Grayscale: 0x00 ; RGB: 0x01)
#   4B width (LE)
#   4B height (LE)
#   <image data>
#
# Image Data:
#   1B length
#   1B value
#
# For RGB images, the data for a Y block is written, then Cb, then Cr.
#
# Image Snake Pattern:
# 0 --> .
# |     .
# v     .
# . . . N

MODE_GRAYSCALE = 0
MODE_RGB = 1

class NCageReader:
    def __init__(self):
        self.size = None
        self.mode = None
        self.size_blocks = None
        self.size_true_blocks = None
        self.blocks_rlc = []

    # I'm lazy, so this is just going to read the whole file into memory.
    def load(self, filename):
        ifile = open(filename, 'rb')
        # Magic, Mode, Width, Height
        header_bytes = ifile.read(5 + 1 + 4 + 4)
        (magic, mode, width, height) = struct.unpack('<5s1B2I', header_bytes)
        if magic != 'NCAGE':
            raise ValueError('This file is like Ice Cube in Are We There Yet?...'
                             + 'Not Nick Cage')
        if mode > MODE_RGB:
            raise ValueError('This mode is not my National Treasure')
        if (width == 0) or (height == 0):
            raise ValueError('Every great story seems to begin with a snake,'
                             + "but something isn't right here")
        # Seems legit
        self.size = (width, height)
        self.mode = mode
        twblocks = width // 8 # Hard coding 8x8 blocks
        thblocks = height // 8
        if (width % 8) != 0:
            wblocks = twblocks + 1
        else:
            wblocks = twblocks
        if (height % 8) != 0:
            hblocks = thblocks + 1
        else:
            hblocks = thblocks
        self.size_true_blocks = (twblocks, thblocks)
        self.size_blocks = (wblocks, hblocks)
        # Read in each RLC block
        a = []
        acount = 0
        while True:
            s = ifile.read(2)
            if s == '':
                break
            (length, value) = struct.unpack('2B', s)
            if acount == 64:
                self.blocks_rlc.append(a)
                a = []
                acount = 0
            a.append( (length, value) )
            acount += length
        if acount == 64:
            self.blocks_rlc.append(a)
        ifile.close()
        return True

    def __getitem__(self, index):
        return self.blocks_rlc[index]

    def __len__(self):
        return len(self.blocks_rlc)


class NCageWriter:
    def __init__(self, filename, width, height, mode):
        self.ofile = open(filename, 'wb')
        header_bytes = struct.pack('<5s1B2I', 'NCAGE', mode, width, height)
        self.ofile.write(header_bytes)

    # Write a block in RLC form...
    def write_block_rlc(self, block_y, block_cb=None, block_cr=None):
        l = [ block_y ]
        if block_cb is not None:
            l.append(block_cb)
        if block_cr is not None:
            l.append(block_cr)
        for block in l:
            for x in block:
                bites = struct.pack('2B', x[0], x[1])
                self.ofile.write(bites)
        return True

    def close(self):
        self.ofile.close()
