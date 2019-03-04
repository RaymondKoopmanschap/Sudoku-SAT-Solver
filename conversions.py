from collections import Counter
import copy
import numpy as np


def Dimacs2CNF(text_file):
    with open(text_file, "r") as f:

        # Read all the comments in the file
        line = f.readline()
        while line[0] == "c":
            line = f.readline()

        # Define number of variables and clauses
        split1 = line.split()
        numVar = int(split1[2])
        numClauses = int(split1[3])

        cl2truth = {}  # {Clause: {1,0} } Each clause is either satisfied (1) or unknown (0)
        lit2cls = {}  # {lit: [list of clauses, each clause is a tuple]See which literal occurs in which clause
        lit2truth = {}  # {lit: {-1,0,1} Each literal is either false (-1), unassigned (0) or true (1).
        atom_count = Counter()  # Keep the count of each atom, e.g. -1, 3, -124. This is for easy pure literal search
        litlist = []  # Make a list of all the literals. Also used for pure literal search

        for line in f:
            split = line.split()
            del split[-1]  # Remove the 0 at the end
            clause = []
            for atom in split:
                atom = int(atom)
                lit = abs(atom)
                clause.append(atom)
                atom_count[atom] += 1
                lit2truth[lit] = 0
                if lit not in litlist:
                    lit2cls[lit] = []
                    litlist.append(lit)
            clause = tuple(clause)
            for i in split:
                lit = abs(int(i))
                lit2cls[lit].append(clause)
            cl2truth[clause] = 0  # Each clause is initially unknown (0)

    satCount = 0
    choices = {}
    choices[111] = copy.deepcopy(lit2truth)
    return [cl2truth, lit2truth, lit2cls, atom_count, litlist, choices], numVar, numClauses


def txt2strings(filepath):
    with open(filepath, "r") as rf:
        sudokus=list()
        for sudoku in rf:
            sudokus.append(sudoku)
    return sudokus


def string2dimacs(sudoku,rulesfilepath,targetfilepath):
    with open(targetfilepath, "w") as wf:
        with open(rulesfilepath,"r") as rulesfile:
            for line in rulesfile:
                wf.write(line)
        row = 1
        column = 1
        for number in sudoku:
            if number.isdigit():
                n = str(row) + str(column) + str(number) + " 0\n"
                wf.write(n)
            if column == 9:
                row = row + 1
                column = 1
                continue
            column = column + 1


def sudoku2dimacs_file(inputfile, lit2truth, num_clauses):
    output_file = inputfile + ".out"
    f= open(output_file,"w+")

    f.write("p cnf " + str(len(lit2truth)) + " " + str(num_clauses) + "\n")

    for lit in lit2truth:
        if lit2truth[lit] == 0:
            lit2truth[lit] = 1
        atom = lit * lit2truth[lit]
        f.write(str(atom) + " 0\n")


def check_sudoku(lit2truth):
    """
    :param lit2truth: dictionary assigning literals to truth values
    :return:
    the next two comments are comment+code from the old implementation
    """

    """
    Check sudoku.
    :param true_vars: List of variables that your system assigned as true. Each var should be in the form of integers.
    :return:
    """
    import math as m
    """
    s = []
    row = []
    for i in range(len(true_vars)):
        row.append(str(int(true_vars[i]) % 10))
        if (i + 1) % 9 == 0:
            s.append(row)
            row = []
    """
    s = np.zeros((9, 9))
    for lit in lit2truth:
        if lit2truth[lit] == 1:
            lit = str(lit)
            row = int(lit[0]) - 1
            column = int(lit[1]) - 1
            number = int(lit[2])
            s[row, column] = number

    correct = True
    for i in range(len(s)):
        for j in range(len(s[0])):
            for x in range(len(s)):
                if i != x and s[i][j] == s[x][j]:
                    correct = False
                    print("Repeated value in column:", j)
            for y in range(len(s[0])):
                if j != y and s[i][j] == s[i][y]:
                    correct = False
                    print("Repeated value in row:", i)
            top_left_x = int(i-i%m.sqrt(len(s)))
            top_left_y = int(j-j%m.sqrt(len(s)))
            for x in range(top_left_x, top_left_x + int(m.sqrt(len(s)))):
                for y in range(top_left_y, top_left_y + int(m.sqrt(len(s)))):
                    if i != x and j != y and s[i][j] == s[x][y]:
                        correct = False
                        print("Repeated value in cell:", (top_left_x, top_left_y))
    return correct