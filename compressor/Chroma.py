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
        print("Hooray you can sample!") #debug obv
        #actual sampling goes here

sample_in = input('Please enter chroma subsampling values as A:B:C - ')
try:
    A1, X1, Y1 =sample_in.split(':', 2)
except ValueError:
    print('This input is invalid.')
    sys.exit(0)
sampling(A1, X1, Y1)
print(A1, X1, Y1)