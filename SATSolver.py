from helper_functions_SAT import *
from txt2dimacs import *
from visualization import *
from printSudoku import check_sudoku
import time
import pandas as pd

filepath="text-files/1000 sudokus.txt"

sudokus=txt2strings(filepath)[:]

node_metrics = {"T/F": [], "CP": [], "CN": [], "choice_depth": [], "num_sat_clauses": [], "lit": [], "good_decision": []}
sudoku_metrics = {"num_steps": []}  # Number of steps is backtracks + 2 (or 1 if it only takes 1 step)

starttime=time.time()

for sudoku in sudokus:
    seconds = time.time()

    # Converting part
    string2dimacs(sudoku,"text-files/sudoku-rules.txt","text-files/sudoku-dimacs_temp.txt")
    CNF, num_var, num_clauses = Dimacs2CNF("text-files/sudoku-dimacs_temp.txt")
    cl2truth, lit2truth, lit2cls, atomCount, litlist, choices = CNF
    print("format preparation took: ", time.time() - seconds)
    seconds = time.time()

    # Algorithm + metrics
    sudoku_metrics_temp = {"num_steps": 0}
    b = DP_algo_naive(CNF, litlist[0], 0, node_metrics, sudoku_metrics_temp)
    update_right_decision(lit2truth, node_metrics, sudoku_metrics)
    update_sudoku_metrics(sudoku_metrics, sudoku_metrics_temp)

    print("solver took: ", time.time() - seconds)  # 0.3 seconds
    # print("solvable: ",b)
    # print(lit2truth)
    # truth2vis(lit2truth)
    # print("solution check successful: ", check_sudoku(lit2truth))
    # wait = input("PRESS ENTER TO CONTINUE.")

df = pd.DataFrame(node_metrics)
print(df)

print("Algorithm took ",time.time()-starttime," seconds.")

df.to_pickle("text-files/dataframe_rand.txt") # save file
