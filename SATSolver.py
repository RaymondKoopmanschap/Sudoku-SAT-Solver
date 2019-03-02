from helper_functions_SAT import *
from visualization import *
import time

seconds = time.time()

CNF = Dimacs2CNF("text-files/sudoku-dimacs.txt")

cl2truth, lit2truth, lit2cls, atomCount, litlist, choices = CNF

#temp = lit2truth.copy()

b = DP_algo_naive(CNF, litlist[0], 0)
print(time.time() - seconds)  # 0.3 seconds
print(b)
print(lit2truth)


