import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Compressor.NCage as N
import TAP

# Testing code for DCT

TAP.comment("Testing NCage module...")
TAP.tests(3)

VAL = [ (64, 0) ]
EXPECT = ( 1, 8, 8, N.MODE_GRAYSCALE )


try:
    foo = N.NCageWriter('test.ncage', 8, 8, N.MODE_GRAYSCALE)
    foo.write_block_rlc( VAL )
    foo.close()
    TAP.expect_pass(True, "Test Simple NCageWriter Grayscale")
except:
    TAP.expect_pass(False, "Test Simple NCageWriter Grayscale")

try:
    foo = N.NCageReader()
    foo.load('test.ncage')
    TAP.expect_pass(
        result=( EXPECT == (len(foo),foo.size[0],foo.size[1],foo.mode) ),
        message="Test Simple NCageReader Grayscale header")
    TAP.expect_pass(
        result=(VAL == foo[0]),
        message="Test Simple NCageReader Grayscale data")
except:
    TAP.expect_pass(
        result=False,
        message="Test Simple NCageReader Grayscale header")
    TAP.expect_pass(
        result=False,
        message="Test Simple NCageReader Grayscale data")

