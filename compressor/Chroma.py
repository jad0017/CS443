import sys

from PIL import Image

def sampling(A, X, Y):
    """
    Define the chroma subsampling to be used... Error checking hell
    """
    try:
        A = int(A)
        X = int(X)
        Y = int(Y)
    except ValueError:
        print('This input is invalid.')
        sys.exit(0)

    if (A < 0) or (X < 0) or (Y < 0):
        print("This value is invalid. Chroma subsampling must use positive integers.")
    elif (A > 4) or (X > 4) or (Y > 4):
        print("This value is invalid. Chroma subsampling must not be greater than 4.")
    elif (A != 4):
        print("This value is invalid. Chroma subsampling must use 4 for its first value.")
    elif (X == 0) and (Y == 0):
        print("4:0:0 subsampling is not possible.. Please enter different numbers.")
    elif (X == 3) or (Y == 3):
        print("3 is not a valid number for chroma subsampling. Please enter different numbers.")
    else:
        if (A==4) and (X==4) and (Y==4):
            print("4:4:4 subsampling") #trivial -- no change, but it's here for completeness

        elif (A==4) and (X==2) and (Y==0):
            print("4:2:0 subsampling")
            yin_420= input('Please enter your file name for the Y channel image, including the extension: ')
            cbin_420= input('Please enter your file name for the Cb channel image, including the extension: ')
            crin_420= input('Please enter your file name for the Cr channel image, including the extension: ')
            #sample_420(yin_420,cbin_420,crin_420)

        elif (A==4) and (X==1) and (Y==1):
            print("4:1:1 subsampling")
            yin_411= input('Please enter your file name for the Y channel image, including the extension: ')
            cbin_411= input('Please enter your file name for the Cb channel image, including the extension: ')
            crin_411= input('Please enter your file name for the Cr channel image, including the extension: ')
            sample_411(cbin_411)
            sample_411(crin_411)

        else:
            print("Something went wrong.")

def sample_411(imgstring):
    """
    Perform 4:1:1 subsampling on an image.
    The actual result is barely noticeable (I couldn't actually tell it had changed anything), but examining it in photoshop, it does perform as expected, thankfully.

    :param imgstring: a string of the target image's name

    :returns: an image with the filenamesubsampled_411_imgstring
    """

    try:
        im = Image.open(imgstring)
    except IOError:
        print('This was an invalid file. Please try again.')
        sys.exit(0)
    # DEBUG: just making sure it's reading images correctly, remove
    #im.show()

    for Y in range (im.size[1]):
        for X in range (im.size[0]):
            i = 1
            if (i == 1):
                (r,g,b) = im.getpixel((X,Y))
                i = i + 1
            elif (1 < i < 4):
                im.putpixel((X,Y), (r,g,b))
                i = i + 1
            else:
                im.putpixel((X,Y), (r,g,b))
                i = 1
            #if imageIndex == 0:
            #    y = min(int(.299*r + .587*g + .144*b), 255)
            #    r = g = b = y

            #im.putpixel((X,Y), (r,g,b))

    outname = "subsampled_411_" + imgstring
    im.save(outname)

sample_in = input('Please enter chroma subsampling values in A:B:C form \nAvaliable values - 4:4:4, 4:2:0, 4:1:1 \nChroma Subsampling - ')
try:
    A1, X1, Y1 =sample_in.split(':', 2)
except ValueError:
    print('This input is invalid.')
    sys.exit(0)
sampling(A1, X1, Y1)
print(A1, X1, Y1) #DEBUG - remove