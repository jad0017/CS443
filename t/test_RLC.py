import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import Compressor.RLC as RLC
import TAP

# Testing code for RLC Matrix

TAP.comment("Testing RLC module...")
TAP.tests(6)

# Test 1
expected_array = RLC.RLC_Tp8
TAP.expect_pass(
    result=(RLC.gen_RLC_translation_array(8) == expected_array),
    message="Verify gen_RLC_translation_array(<even>) matches expected array"
)
# Test 2
expected_array = [
    (0,0),
    (0,1), (1,0),
    (2,0), (1,1), (0,2),
    (1,2), (2,1),
    (2,2),
]
TAP.expect_pass(
    result=(RLC.gen_RLC_translation_array(3) == expected_array),
    message="Verify gen_RLC_translation_array(<odd>) matches expected array"
)
# Test 3
input_matrix = [
    [ 1, 1, 1 ],
    [ 1, 1, 1 ],
    [ 1, 1, 1 ],
]
expected_array = [ (9, 1) ]
TAP.expect_pass(
    result=(RLC.RLC(input_matrix) == expected_array),
    message="Verify RLC(<simple>) matches expected array"
)
# Test 4
input_matrix = [
    [ 12, 23,  3, 99 ],
    [ 14,  3, 99, 99 ],
    [  3, 99, 99, 99 ],
    [ 99, 99, 99, 99 ],
]
expected_array = [ (1, 12), (1, 23), (1, 14), (3, 3), (10, 99) ]
TAP.expect_pass(
    result=(RLC.RLC(input_matrix) == expected_array),
    message="Verify RLC(<complex>) matches expected array"
)
# Test 5
input_array = [ (9, 1) ]
expected_matrix = [
    [ 1, 1, 1 ],
    [ 1, 1, 1 ],
    [ 1, 1, 1 ],
]
TAP.expect_pass(
    result=(RLC.iRLC(input_array) == expected_matrix),
    message="Verify iRLC(<simple>) matches expected matrix"
)
# Test 6
input_array = [ (1, 12), (1, 23), (1, 14), (3, 3), (10, 99) ]
expected_matrix = [
    [ 12, 23,  3, 99 ],
    [ 14,  3, 99, 99 ],
    [  3, 99, 99, 99 ],
    [ 99, 99, 99, 99 ],
]
TAP.expect_pass(
    result=(RLC.iRLC(input_array) == expected_matrix),
    message="Verify iRLC(<complex>) matches expected matrix"
)


