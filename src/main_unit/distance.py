import math

def distance_left(x):
    #z = (x-49.0)/31.0
    return distance_both(x)
#return (0.14*(z**6))-(0.96*(z**5))+(2.4*(z**4))-(3.2*(z**3))+(4.4*(z**2))-(8.3*z) + 13


def distance_right(x):
    return distance_both(x)    
#z = (x-50.0)/31.0
    #return (0.041*(z**6))-(0.38*(z**5))+(1.5*(z**4))-(3.3*(z**3))+(5.3*(z**2))-(8.3*z) + 13

def distance_both(x):
    return 76*math.exp(x*(-0.1))+20*math.exp(x*(-0.015))
