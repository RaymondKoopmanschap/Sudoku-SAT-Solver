#!/usr/bin/python
# coding: utf-8

import sys
from helper_functions_SAT import *
from visualization import *
from lit2truth2DIMACS import generate_output_file

try:
    solver = (sys.argv[1])
    inputfile = (sys.argv[2])
except:
    print("Please specify input file")

print(solver)

node_metrics = {"T/F": [], "CP": [], "CN": [], "choice_depth": [], "num_sat_clauses": [], "lit": [], "good_decision": []}
sudoku_metrics = {"num_steps": []}  # Number of steps is backtracks + 2 (or 1 if it only takes 1 step)


CNF, num_var, num_clauses = Dimacs2CNF(inputfile)
cl2truth, lit2truth, lit2cls, atomCount, litlist, choices = CNF

# Algorithm + metrics
bool = False
sudoku_metrics_temp = {"num_steps": 0}
if solver == "-S1":
    bool = DP_algo_naive(CNF, litlist[0], 0, node_metrics, sudoku_metrics_temp)

# truth2vis(lit2truth)
if bool:
    generate_output_file(inputfile, lit2truth, num_clauses)
else:
    output_file = inputfile + ".out"
    f = open(output_file, "w+")




