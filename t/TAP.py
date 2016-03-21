
TEST_NUM = 1

def tests(N):
    print "1.." + str(N)


def todo(message):
    global TEST_NUM
    print "not ok", str(TEST_NUM), "#TODO", message
    TEST_NUM += 1


def expect_pass(result, message=""):
    global TEST_NUM
    if result == True:
        print "ok", str(TEST_NUM), message
    else:
        print "not ok", str(TEST_NUM), message
    TEST_NUM += 1


def expect_fail(result, message=""):
    global TEST_NUM
    if result == False:
        print "ok", str(TEST_NUM), message
    else:
        print "not ok", str(TEST_NUM), message
    TEST_NUM += 1


def comment(message):
    print "#", message


