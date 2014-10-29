import distance

UPPER_LINE_LIMIT = 0.6
LOWER_LINE_LIMIT = 0.4

RIGHT = "RIGHT"
LEFT = "LEFT"
NO_STATION = "NO_STATION"
NO_PACKAGE = "NO_PACKAGE"

def convert_line_values(seq):
    res = []
    for e in seq:
        if e < LOWER_LINE_LIMIT:
            res.append(False)
        elif e > UPPER_LINE_LIMIT:
            res.append(True)
        else:
            res.append(None)
    return res

def all_equal(seq):
    t = seq[0]

    for e in seq:
        if e != t:
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
    left = seq[0:3]
    center = seq[4:7]
    right = seq[8:]

    n_left = sum(e for e in left if e is not None)
    n_center = sum(e for e in center if e is not None)
    n_right = sum(e for e in right if e is not None)

    if n_left >= 2 and n_center >= 1:
        return LEFT
    elif n_right >= 2 and n_center >= 1:
        return RIGHT
    else:
        return NO_STATION


def station_center(center_seq, front_seq):
    front_left = front_seq[0:3]
    front_center = front_seq[4:7]
    front_right = front_seq[8:]

    n_front_left = sum(e for e in front_left if e is not None)
    n_front_center = sum(e for e in front_center if e is not None)
    n_front_right = sum(e for e in front_right if e is not None)

    if n_front_center >= 1 and (n_front_left + n_front_right) <= 1:
        left = center_seq[0]
        right = center_seq[1]

        return station(left, right)
    else:
        return station(False, False)

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
