from z3 import *

v1 = Int('v1')
v2 = Int('v2')

v = [[[Int(f"v_{i}{j}{k}") for i in range(9)] for j in range(9)] for k in range(9)]

sum11 = v_{i}{j}{}

s = Solver()

s.add(sum11 = 1)

