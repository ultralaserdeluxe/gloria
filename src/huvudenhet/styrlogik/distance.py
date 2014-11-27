def distance_left(x):
    z = (x-41.0)/25.0
    return (0.093*(z**6)) - (0.77*(z**5)) + (2.4*(z**4)) - (3.9*(z**3)) + (4.7*(z**2)) - (7.4*z) + 13

#for x in range(17,110):
#    print "x = " + str(x) + " distance = " + str(kastman(x))


def distance_right(x):
    z = (x-40.0)/23.0
    return (0.83*(z**4)) - (4.2*(z**3)) + (7*(z**2)) - (7.5*z) + 12

#for x in range(1,110):
#    print "x = " + str(x) + " distance = " + str(kastman_right(x))

