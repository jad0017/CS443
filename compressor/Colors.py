import sys
import shutil
import os
import struct

from PIL import Image

def usage():
	print("Usage: %s filename.jpg" % (sys.argv[0]))
	exit()

def rgb_to_ycbcr(fname, outname, imageIndex):
	im = Image.open(fname) #Can be many different formats.
	for Y in range (im.size[1]):
		for X in range (im.size[0]):
			(r,g,b) = im.getpixel((X,Y))

			if imageIndex == 0:
				y = min(int(.299*r + .587*g + .144*b), 255)
				r = g = b = y
			elif imageIndex == 1:
				cb = int((-.168736*r) + (-.331264*g) + (b/2.0) + 128)
				r = g = 255 - cb
				b = cb
			else:
				cr = int((.5*r) + (-.418688*g) + (-.081312*b) + 128)
				b = g = 255 - cr
				r = cr

			im.putpixel((X,Y), (r,g,b))

	im.save(outname)

fname = sys.argv[1]
oname = fname.split(".")
y = oname[0] + "_y." + oname[-1]
cb = oname[0] + "_cb." + oname[-1]
cr = oname[0] + "_cr." + oname[-1]

rgb_to_ycbcr(fname,y, 0)
rgb_to_ycbcr(fname,cb, 1)
rgb_to_ycbcr(fname,cr, 2)