from collections import Counter

def Dimacs2CNF(textfile):
    with open(textfile, "r") as f:

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
            del split[-1] #Remove the 0 at the end
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

    # TODO add satCount, numClauses, lit2cls:
    satCount = 0
    choices = []
    return [cl2truth, lit2truth, lit2cls, atom_count, litlist, choices]


def clause_satisfied(clause, lit2truth):
    for atom in clause:
        lit = abs(atom)
        if atom * lit2truth[lit] > 0:  # Same sign check, if same sign then clause is satisfied
            return True
    return False


def satisfied_naive(cl2truth, lit2truth):
    for clause in cl2truth:
        if not clause_satisfied(clause, lit2truth):
            return False
    return True


def clause_is_empty(lit2truth, clause):
    for atom in clause:
        lit = abs(atom)
        if lit2truth[lit] == 0:
            return False # If a literal is unassigned, then can never be empty
        if (lit2truth[lit] * atom) > 0:
            return False # If truth is 1 and atom is 1 then not empty, same with -1 and -1

    return True  # If no literal is true or unknown then it is false


def empty_clauses_naive(cl2truth, lit2truth, lit2cls, lit):
    for clause in lit2cls[lit]:
        if clause_is_empty(lit2truth, clause):
            return True
    return False


def update_naive(lit2truth, lit, truth, choices):
    lit2truth[lit] = truth  # Assign new given truth value

    # Unassign the last choice you made, because you are higher up in the tree
    if len(choices) == 0:
        return
    last_choice = choices[-1]
    while lit != last_choice:
        lit2truth[last_choice] = 0
        choices.remove(last_choice)
        last_choice = choices[-1]


def choose_value(lit2truth):
    for lit in lit2truth:
        if lit2truth[lit] == 0:
            return lit


def DP_algo_naive(CNF, lit, truth):
    cl2truth, lit2truth, lit2cls, atom_count, litlist, choices = CNF
    # print(lit2truth, lit, truth, choices)
    update_naive(lit2truth, lit, truth, choices)  # Update lit2truth
    if satisfied_naive(cl2truth, lit2truth):
        return True
    if empty_clauses_naive(cl2truth, lit2truth, lit2cls, lit):
        return False
    lit = choose_value(lit2truth)
    choices.append(lit)
    CNF = cl2truth, lit2truth, lit2cls, atom_count, litlist, choices
    return DP_algo_naive(CNF, lit, 1) or DP_algo_naive(CNF, lit, -1)


"""For later use"""

# Given a truth assignment, see if the clause is satisfied
# Returns the variable that needs to be changed and output 0 if no unit clause.
def unit_clause(lit2truth, clause):
    unit = 0
    counter = 1
    for atom in clause:
        lit = abs(atom)
        if lit2truth[lit] == 0:
            unit = lit
            counter = counter + 1
    if counter == 1:
        return unit
    return unit


def unit_propagation(cl2truth, lit2truth):
    unit_clause_list = []
    for clause in cl2truth:  # TODO Can optimize by checking if clause already satisfied
        return


def check_pure_literal(atomCount, litlist):
    for i in litlist:
        lit = str(i)
        posCount = atomCount[lit]
        negCount = atomCount["-" + lit]
        if posCount == 0 and negCount != 0:  # No positive counts of specific literal so set to negative
            return lit, False
        if negCount == 0 and posCount != 0:  # Vice Versa
            return lit, True


def update_clause(lit, boolean, clause, cl2truth):
    lit = lit * boolean  # boolean is 1 or -1, if -1 then atom becomes -1, thus negative
    for atom in clause:
        if atom == lit:
            cl2truth[clause] = 1


def update(lit, boolean, lit2truth, lit2cls, cl2truth):
    listofunits = [(lit, boolean)]
    while len(listofunits) == 0:
        lit = listofunits[0][0]
        boolean = listofunits[0][1]
        lit2truth[lit] = boolean
        clauses = lit2cls[lit]
        for clause in clauses:
            if cl2truth[clause] == 1:
                continue
            if clause_is_empty(lit2truth, clause):
                return False
            unit = unit_clause(lit2truth, clause)
            if unit != 0:
                listofunits.append(unit)
                continue
            else:
                update_clause(lit, boolean, clause, cl2truth)


def satisfied(satCount, numClauses):
    return satCount == numClauses