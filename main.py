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

def print_image_mode(img):
    mode = img.mode
    if mode == '1':
        print("1-bit(black and white)")
    elif mode == 'L':
        print("Grayscale (Luminosity)")
    elif mode == 'RGB':
        print("RGB")
    elif mode == 'RGBA':
        print("RGBA")
    elif mode == 'P':
        print("Palette")
    else:
        print("Some other mode:", mode)


# Example of reading image data
def print_pixels(img):
    (width, height) = img.size
    img_pixels = img.load()
    for x in range(width):
        for y in range(height):
            pixel = img_pixels[x, y]
            sys.stdout.write('Pixel[%d, %d]: ( ' % (x, y))
            for p in pixel:
                sys.stdout.write('%d ' % (p,) )
            sys.stdout.write(')\n')
            sys.stdout.flush()


# Example of writing image data
def blacken_image(img):
    (width, height) = img.size
    img_pixels = img.load()
    for x in range(width):
        for y in range(height):
            pixel = img_pixels[x, y]
            # Zero out the tuple. (RGB and RGBA only)
            # L, 1, and P all take single values (int)
            pixel = (0,) * len(pixel)
            img_pixels[x, y] = pixel


def print_pixel(img, pixels, x, y):
    mode = img.mode
    if mode == '1':
        sys.stdout.write('%d ' % (pixels[x,y],))
    elif mode == 'L':
        sys.stdout.write('%03d ' % (pixels[x,y],))
    elif mode == 'RGB':
        sys.stdout.write('(%03d,%03d,%03d) ' % pixels[x,y])
    elif mode == 'RGBA':
        sys.stdout.write('(%03d,%03d,%03d,%03d) ' % pixels[x,y])
    elif mode == 'P':
        sys.stdout.write('%03d ' % (pixels[x,y],))
    else:
        sys.stdout.write('U ')


def print_empty_pixel(img):
    mode = img.mode
    if mode == '1':
        sys.stdout.write('- ')
    elif mode == 'L':
        sys.stdout.write('--- ')
    elif mode == 'RGB':
        sys.stdout.write('(---,---,---) ')
    elif mode == 'RGBA':
        sys.stdout.write('(---,---,---,---) ')
    elif mode == 'P':
        sys.stdout.write('--- ')
    else:
        sys.stdout.write('- ')


def print_block(img, pixels, xb, yb, N):
    x_off = N * xb
    y_off = N * yb

    for y in range(y_off, y_off + N):
        sys.stdout.write('[ ')
        for x in range(x_off, x_off + N):
            print_pixel(img, pixels, x, y)
        sys.stdout.write(']\n')
        sys.stdout.flush()


def print_block_partial_width(img, pixels, x_off, yb, N):
    (width, height) = img.size
    xlen = width - x_off
    xolen = N - xlen
    y_off = N * yb

    for y in range(y_off, y_off + N):
        sys.stdout.write('[ ')
        for xo in range(xlen):
            print_pixel(img, pixels, x_off + xo, y)
        for xo in range(xolen):
            print_empty_pixel(img)
        sys.stdout.write(']\n')
        sys.stdout.flush()


def print_block_partial_height(img, pixels, xb, y_off, N):
    (width, height) = img.size
    ylen = height - y_off
    yolen = N - ylen
    x_off = N * xb

    for yo in range(ylen):
        sys.stdout.write('[ ')
        for x in range(x_off, x_off + N):
            print_pixel(img, pixels, x, y_off + yo)
        sys.stdout.write(']\n')
        sys.stdout.flush()
    for yo in range(yolen):
        sys.stdout.write('[ ')
        for x in range(N):
            print_empty_pixel(img)
        sys.stdout.write(']\n')
        sys.stdout.flush()


def print_block_bottom_right(img, pixels, x_off, y_off, N):
    (width, height) = img.size

    xlen = width - x_off
    xolen = N - xlen

    ylen = height - y_off
    yolen = N - ylen

    for yo in range(ylen):
        sys.stdout.write('[ ')
        for xo in range(xlen):
            print_pixel(img, pixels, x_off + xo, y_off + yo)
        for xo in range(xolen):
            print_empty_pixel(img)
        sys.stdout.write(']\n')
        sys.stdout.flush()
    for yo in range(yolen):
        sys.stdout.write('[ ')
        for x in range(N):
            print_empty_pixel(img)
        sys.stdout.write(']\n')
        sys.stdout.flush()


# Loop over image pixels and print each NxN block.
def block_image(img, N):
    (width, height) = img.size

    width_off = N - (width % N)
    if width_off == 8:
        width_off = 0
    width_off_pos = width - (width % N)
    width_blocks = width // N

    height_off = N - (height % N)
    if height_off == 8:
        height_off = 0
    height_off_pos = height - (height % N)
    height_blocks = height // N

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
            print("Block(%d, %d):" % (xb, yb))
            print_block(img, pixels, xb, yb, N)
        # Address partial width block
        if width_off != 0:
            print("Block(%d, %d):" % (width_blocks, yb))
            print_block_partial_width(img, pixels, width_off_pos, yb, N)
    if height_off != 0:
        for xb in range(width_blocks):
            print("Block(%d, %d):" % (xb, height_blocks))
            print_block_partial_height(img, pixels, xb, height_off_pos, N)
        if width_off != 0:
            print("Block(%d, %d):" % (width_blocks, height_blocks))
            print_block_bottom_right(img, pixels, width_off_pos, height_off_pos, N)


if (len(sys.argv) < 2) or (len(sys.argv) > 3):
    print("Usage: {} <input> [output]".format(sys.argv[0]))
    sys.exit(1)

infile = sys.argv[1]

if len(sys.argv) == 3:
    outfile = sys.argv[2]
else:
    outfile = None


img = Image.open(infile)

print_image_mode(img)
#print_pixels(img)
#blacken_image(img)
block_image(img, 8)

if outfile is not None:
    img.save(outfile)

sys.exit(0)
