import distance

UPPER_LINE_LIMIT = 0.8
LOWER_LINE_LIMIT = 0.3

RIGHT = "RIGHT"
LEFT = "LEFT"
NO_STATION = "NO_STATION"
NO_PACKAGE = "NO_PACKAGE"

def convert_line_values(seq):
    res = []
    for e in seq:
        if e < LOWER_LINE_LIMIT:
            res.append(True)
        elif e > UPPER_LINE_LIMIT:
            res.append(False)
        else:
            res.append(None)
    return res

def all_equal(seq):
    t = seq[0]

    for e in seq:
        if e != t:    if seq[0] == True
            return False
    return True

def station(left, right):
    if left == True and right == False:
        return LEFT
    elif left == False and right == True:
        return RIGHT
    else:
        return NO_STATION

def station_front(seq):
    left = seq[2]
    right = seq[8]

    return station(left, right)

def station_center(seq):
    left = seq[0]
    right = seq[1]
    
    return station(left, right)

def detect_package(left_value, right_value):
    if distance.distance_left(left_value) <= 20.0:
        return LEFT
    elif distance.distance_right(right_value) <= 20.0:
        return RIGHT
    else:
        return NO_PACKAGE

if __name__ == "__main__":
    different = [0.1, 0.9, 0.6, 0.2]
    converted = convert_line_values(different)
    print converted
    print all_equal(converted)

    equal = [0.1, 0.2, 0.0]
    converted = convert_line_values(equal)
    print converted
    print all_equal(converted)
