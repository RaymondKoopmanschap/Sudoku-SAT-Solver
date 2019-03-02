from helper_functions_SAT import *
from txt2dimacs import *
from visualization import *
from printSudoku import check_sudoku
import time

filepath="text-files/1000 sudokus.txt"

sudokus=txt2strings(filepath)

for sudoku in sudokus:
    seconds = time.time()
    string2dimacs(sudoku,"text-files/sudoku-rules.txt","text-files/sudoku-dimacs_temp.txt")

    CNF = Dimacs2CNF("text-files/sudoku-dimacs_temp.txt")


    print("format preparation took: ", time.time() - seconds)
    seconds = time.time()

    cl2truth, lit2truth, lit2cls, atomCount, litlist, choices = CNF

    #temp = lit2truth.copy()

    b = DP_algo_naive(CNF, litlist[0], 0)
    print("solver took: ", time.time() - seconds)  # 0.3 seconds
    print("solvable: ",b)
    #print(lit2truth)
    #truth2vis(lit2truth)
    print("solution check successful: ", check_sudoku(lit2truth))
    wait = input("PRESS ENTER TO CONTINUE.")


