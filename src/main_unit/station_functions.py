import distance

UPPER_LINE_LIMIT = 0.6
LOWER_LINE_LIMIT = 0.4

TROSKEL_VALUE = 4

RIGHT = 1
LEFT = -1
NO_STATION = 0
NO_PACKAGE = "NO_PACKAGE"

class LineDetector:
    def __init__(self):
        self.past_front = [[0]*11]*6
        self.past_center = [[0]*2]*6

    def add_values(self, front_values, center_values):
        self.past_front.pop(0)

        front_converted = self.convert_line_values(front_values)
        self.past_front.append(front_converted)

        self.past_center.pop(0)

        center_converted = self.convert_line_values(center_values)
        self.past_center.append(center_converted)

    def convert_line_values(self, seq):
        res = []
        for e in seq:
            if e < LOWER_LINE_LIMIT:
                res.append(False)
            elif e > UPPER_LINE_LIMIT:
                res.append(True)
            else:
                res.append(None)
        return res

    def all_equal_one(self, seq):
        t = seq[0]

        for e in seq:
            if e != t:
                return False
        return True

    def all_equal_front(self):
        r = [self.all_equal_one(p) for p in self.past_front]

        return sum(r) >= TROSKEL_VALUE

    def all_equal_center(self):
        r = [self.all_equal_one(p) for p in self.past_center]

        return sum(r) >= TROSKEL_VALUE

    def station(self, left, right):
        if left == True and right == False:
            return LEFT
        elif left == False and right == True:
            return RIGHT
        else:
            return NO_STATION

    def station_front_one(self, seq):
        left = seq[0:4]
        center = seq[4:7]
        right = seq[7:]

        n_left = sum(e for e in left if e is not None)
        n_center = sum(e for e in center if e is not None)
        n_right = sum(e for e in right if e is not None)

        if n_left >= 3 and n_center >= 1 and n_right <= 2:
            return LEFT
        elif n_left <= 2 and n_center >= 1 and n_right >= 3:
            return RIGHT
        else:
            return NO_STATION

    def station_front(self):
        # If all sensors are covered it is not a station.
        for past in self.past_front:
            u = [e for e in past if e is not None]
            if self.all_equal_one(u):
                return NO_STATION

        r = [self.station_front_one(p) for p in self.past_front]

        s = sum(r)

        if s <= -TROSKEL_VALUE:
            return LEFT
        elif s >= TROSKEL_VALUE:
            return RIGHT
        else:
            return NO_STATION

    def station_center_one(self, center_seq, front_seq):
        center_seq = self.convert_line_values(center_seq)
        front_seq = self.convert_line_values(front_seq)

        front_left = front_seq[0:3]
        front_center = front_seq[4:7]
        front_right = front_seq[8:]

        n_front_left = sum(e for e in front_left if e is not None)
        n_front_center = sum(e for e in front_center if e is not None)
        n_front_right = sum(e for e in front_right if e is not None)

        if n_front_center >= 1 or self.all_equal_one(front_seq):
            left = center_seq[0]
            right = center_seq[1]

            return self.station(left, right)
        else:
            return self.station(False, False)

    def station_center(self):
        r = []
        for i in range(len(self.past_front)):
            t = self.station_center_one(self.past_center[i], self.past_front[i])
            r.append(t)

        s = sum(r)

        if s <= -TROSKEL_VALUE:
            return LEFT
        elif s >= TROSKEL_VALUE:
            return RIGHT
        else:
            return NO_STATION

def detect_package(left_value, right_value):
    if distance.distance_left(left_value) <= 20.0:
        return LEFT
    elif distance.distance_right(right_value) <= 20.0:
        return RIGHT
    else:
        return NO_PACKAGE

