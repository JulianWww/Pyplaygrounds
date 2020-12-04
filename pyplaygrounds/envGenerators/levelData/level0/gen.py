import numpy as np
import random

num = random.randint(3,10)

def map():
    arr= np.ones((1, num))
    return arr

def gems():
    return [(0, num-1)]

def pawns():
    return [((0,0), random.randint(0, 3))]

print("loaded generator")
