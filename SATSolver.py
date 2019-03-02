from helper_functions_SAT import *
from txt2dimacs import *
from visualization import *
import time

filepath="text-files/1000 sudokus.txt"

sudokus=txt2strings(filepath)

for sudoku in sudokus:
    seconds = time.time()
    string2dimacs(sudoku,"text-files/sudoku-rules.txt","text-files/sudoku-dimacs_temp.txt")

    CNF = Dimacs2CNF("text-files/sudoku-dimacs_temp.txt")

    seconds = time.time()
    print(time.time() - seconds)

    cl2truth, lit2truth, lit2cls, atomCount, litlist, choices = CNF

    #temp = lit2truth.copy()

    b = DP_algo_naive(CNF, litlist[0], 0)
    print(time.time() - seconds)  # 0.3 seconds
    print(b)
    print(lit2truth)

    truth2vis(lit2truth)
    wait = input("PRESS ENTER TO CONTINUE.")


