import numpy as np

def truth2vis(lit2truth):
    vis = np.zeros((9, 9))
    for lit in lit2truth:
        if lit2truth[lit] == 1:
            lit = str(lit)
            row = int(lit[0]) - 1
            column = int(lit[1]) - 1
            number = int(lit[2])
            vis[row, column] = number

    vis = vis.astype(int)
    for count, row in enumerate(vis):
        if count % 3 == 0 and count != 0:
            print()
        for count2, i in enumerate(row):
            if count2 % 3 == 0:
                print(" ", end="")
            print(str(i) + " ", end="")
        print()


def dimacs2vis(file):
    with open(file, "r") as file:
        vis = np.zeros((9, 9))
        for num in file:
            row = int(num[0]) - 1
            column = int(num[1]) - 1
            number = num[2]
            vis[row, column] = number

    vis = vis.astype(int)
    for count, row in enumerate(vis):
        if count % 3 == 0 and count != 0:
            print()
        for count2, i in enumerate(row):
            if count2 % 3 == 0:
                print(" ", end="")
            print(str(i) + " ", end="")
        print()