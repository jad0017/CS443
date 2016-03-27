#The PIL python library is required to run this script.

import sys
import shutil
import os
import struct

from PIL import Image

def usage():
	print "Usage: %s file1.jpg file2.jpg" % (sys.argv[0])
	exit()

def mse(img1, img2):
	im1 = Image.open(img1)
	im2 = Image.open(img2)
	rsum = 0
	gsum = 0
	bsum = 0

	if not im1.size == im2.size:
		print "Images are different sizes"
		exit(1)

	for Y in range (im1.size[1]):
		for X in range (im1.size[0]):
			(r1,g1,b1) = im1.getpixel((X,Y))
			(r2,g2,b2) = im2.getpixel((X,Y))
			rsum += pow(r1-r2,2)
			gsum += pow(g1-g2,2)
			bsum += pow(b1-b2,2)

	scalar = (im1.size[0] * im2.size[1])

	return (rsum/scalar,gsum/scalar,bsum/scalar)
	

if not len(sys.argv) is 3:
	usage()
	exit(1)

print mse(sys.argv[1], sys.argv[2])
