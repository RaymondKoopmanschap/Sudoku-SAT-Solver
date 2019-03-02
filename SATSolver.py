from helper_functions_SAT import *
from txt2dimacs import *
from visualization import *
from printSudoku import check_sudoku
import pandas as pd
import time

filepath="text-files/1000 sudokus.txt"

sudokus=txt2strings(filepath)[:2]

node_metrics = {"T/F": [], "CP": [], "CN": [], "choice_depth": []}
sudoku_metrics = {"num_steps": []}  # Number of steps is backtracks + 2 (or 1 if it only takes 1 step)

for sudoku in sudokus:
    seconds = time.time()

    # Converting part
    string2dimacs(sudoku,"text-files/sudoku-rules.txt","text-files/sudoku-dimacs_temp.txt")
    CNF = Dimacs2CNF("text-files/sudoku-dimacs_temp.txt")
    cl2truth, lit2truth, lit2cls, atomCount, litlist, choices = CNF
    # print("format preparation took: ", time.time() - seconds)
    seconds = time.time()

    # Algorithm + metrics
    sudoku_metrics_temp = {"num_steps": 0}
    b = DP_algo_naive(CNF, litlist[0], 0, node_metrics, sudoku_metrics_temp)
    update_sudoku_metrics(sudoku_metrics, sudoku_metrics_temp)

    print(node_metrics)
    print(sudoku_metrics)

    # print("solver took: ", time.time() - seconds)  # 0.3 seconds
    # print("solvable: ",b)
    # print(lit2truth)
    # truth2vis(lit2truth)
    # print("solution check successful: ", check_sudoku(lit2truth))
    #wait = input("PRESS ENTER TO CONTINUE.")

df = pd.DataFrame(node_metrics)
# maxCP = 5, always the same
# maxCP = 32, always the same


df.to_pickle("text-files/dataframe1.txt") # save file
import pandas as pd
df = pd.read_pickle("text-files/dataframe1.txt")

from sklearn import linear_model
print(df)
#import statsmodels.formula.api as sm
#from pandas.stats.api import ols
reg = linear_model.LinearRegression()
reg.fit(df[['CP','CN','T/F']], df['choice_depth'])

print(reg.coef_)