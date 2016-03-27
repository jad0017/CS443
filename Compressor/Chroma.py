import sys

from PIL import Image
import Compressor.Matrix

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
            sample_420(cbin_420)
            sample_420(crin_420)

        elif (A==4) and (X==1) and (Y==1):
            print("4:1:1 subsampling")
            yin_411= input('Please enter your file name for the Y channel image, including the extension: ')
            cbin_411= input('Please enter your file name for the Cb channel image, including the extension: ')
            crin_411= input('Please enter your file name for the Cr channel image, including the extension: ')
            sample_411(cbin_411)
            sample_411(crin_411)

        else:
            print("Something went wrong.")

def sample_420(M):
    """
    Perform 4:2:0 subsampling on an image.

    :param M: Matrix to perform sampling on.

    :returns: SampledMatrix: a matrix with the subsampled data
    """
    SampledMatrix = Compressor.Matrix.zero_matrix(len(M[0]), len(M))

    for Y in range (len(M)):
        if (Y % 2) == 0: #if it's the first row, then copy every other pixel
            for X in range (len(M[0])):
                i = 1
                if (i == 1):
                    (r,g,b) = M[Y][X]
                    SampledMatrix[Y][X] = (r,g,b)
                    i = i + 1
                else:
                    SampledMatrix[Y][X] = (r,g,b)
                    i = 1

        else: #if it's an even row, then copy pixel from the row above it
            for X in range (len(M[0])):
                (r,g,b) = M[Y-1][X]
                SampledMatrix[Y][X] = (r,g,b)

    return SampledMatrix

def sample_411(M):
    """
    Perform 4:1:1 subsampling on an image.
    The actual result is barely noticeable (I couldn't actually tell it had changed anything), but examining it in photoshop, it does perform as expected, thankfully.

    :param M: Matrix to perform sampling on.

    :returns: SampledMatrix: a matrix with the subsampled data
    """

    SampledMatrix = Compressor.Matrix.zero_matrix(len(M[0]), len(M))

    for Y in range (len(M)):
        for X in range (len(M[0])):
            if (X % 4) == 0:
                (r,g,b) = M[Y][X]
                SampledMatrix[Y][X] = (r,g,b)
            else:
                SampledMatrix[Y][X] = (r,g,b)

    return SampledMatrix

sample_in = input('Please enter chroma subsampling values in A:B:C form \nAvaliable values - 4:4:4, 4:2:0, 4:1:1 \nChroma Subsampling - ')
try:
    A1, X1, Y1 =sample_in.split(':', 2)
except ValueError:
    print('This input is invalid.')
    sys.exit(0)
sampling(A1, X1, Y1)
print(A1, X1, Y1) #DEBUG - remove