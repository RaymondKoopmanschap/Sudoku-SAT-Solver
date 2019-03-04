from helper_functions_SAT import *
from conversions import *
import time
import pandas as pd


filepath="text-files/1000 sudokus.txt"

sudokus=txt2strings(filepath)[:20]

node_metrics = {"T/F": [], "CP": [], "CN": [], "choice_depth": [], "num_unsat_clauses": [], "lit": [], "good_decision": [], "num_steps": []}
step_counter = {"num_steps": []}  # Number of steps is backtracks + 2 (or 1 if it only takes 1 step)

starttime=time.time()

for sudoku in sudokus:
    seconds = time.time()

    # Converting part
    string2dimacs(sudoku,"text-files/sudoku-rules.txt","text-files/sudoku-dimacs_temp.txt")
    CNF, numvar, numclauses = Dimacs2CNF("text-files/sudoku-dimacs_temp.txt")
    cl2truth, lit2truth, lit2cls, atomCount, litlist, choices = CNF
    step_counter_temp = {"num_steps": 0}
    step_counter_node = Counter()
    #print("format preparation took: ", time.time() - seconds)
    seconds = time.time()

    # Algorithm
    # Heuristics: "standard", "random", "own", "DLCS", "DLIS", "JWOS", "MOM"
    b = davis_putnam(CNF, litlist[0], 0, node_metrics, step_counter_temp, step_counter_node, heuristic="own")

    # Update metrics
    update_right_decision(lit2truth, node_metrics, step_counter, step_counter_temp)
    update_step_counter(step_counter, step_counter_temp)
    print("solver took: ", time.time() - seconds)  # 0.3 seconds

    # print("solvable: ",b)
    # print(lit2truth)
    # truth2vis(lit2truth)
    print("solution check successful: ", check_sudoku(lit2truth))
    # wait = input("PRESS ENTER TO CONTINUE.")

df = pd.DataFrame(node_metrics)
da = pd.DataFrame(step_counter)
print(df)
#print(da)
print(sum(step_counter["num_steps"]))
print("Algorithm took", sum(step_counter['num_steps']), "steps for all sudokus.")
print("Algorithm took", time.time()-starttime, "seconds for all sudokus.")

df.to_pickle("text-files/dataframe_rand.txt")  # save file
