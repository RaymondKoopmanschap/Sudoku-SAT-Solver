from collections import Counter
import copy


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
    choices["begin"] = copy.deepcopy(lit2truth)
    return [cl2truth, lit2truth, lit2cls, atom_count, litlist, choices]


###################################################################################################################
"Satisfaction and empty checks"
###################################################################################################################


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
            return False  # If a literal is unassigned, then can never be empty
        if (lit2truth[lit] * atom) > 0:
            return False  # If truth is 1 and atom is 1 then not empty, same with -1 and -1

    return True  # If no literal is true or unknown then it is false


def empty_clauses_naive(lit2truth, lit2cls, lit):
    for clause in lit2cls[lit]:
        if clause_is_empty(lit2truth, clause):
            return True
    return False


###################################################################################################################
"Updates and choose value"
###################################################################################################################


def update_truth_values(lit2truth, lit, truth, choices):
    #  Unassign the last choice you made, because you are higher up in the tree
    if len(choices) == 1:
        for i in choices["begin"]:
            lit2truth[i] = choices["begin"][i]
            return
    for i in choices[lit]:
        lit2truth[i] = choices[lit][i]
    lit2truth[lit] = truth  # Assign new given truth value


def choose_value(lit2truth):
    for lit in lit2truth:
        if lit2truth[lit] == 0:
            return lit


def update_node_metrics(node_metrics, truth, atom_count, lit, choices, num_sat_clauses):
    """Track desired metrics
    Uncomment lines if you don't want to track them and speed up process"""
    node_metrics["T/F"].append(truth)
    node_metrics["CP"].append(atom_count[lit])
    node_metrics["CN"].append(atom_count[-lit])
    node_metrics["choice_depth"].append(len(choices) - 1)
    node_metrics["num_sat_clauses"].append(num_sat_clauses)
    node_metrics["lit"].append(lit)


def update_sudoku_metrics_temp(sudoku_metrics):
    sudoku_metrics["num_steps"] += 1


def update_sudoku_metrics(sudoku_metrics, sudoku_metrics_temp):
    sudoku_metrics["num_steps"].append(sudoku_metrics_temp["num_steps"])


def update_atom_count(cl2truth, lit2truth, atom_count):
    num_sat_clauses = len(cl2truth)
    atom_count.clear()
    for clause in cl2truth:
        if not clause_satisfied(clause, lit2truth):
            num_sat_clauses -= 1
            for atom in clause:
                atom_count[atom] += 1
    return num_sat_clauses

def update_right_decision(lit2truth, node_metrics, sudoku_metrics):
    litlist = node_metrics["lit"]
    begin = sum(sudoku_metrics["num_steps"])
    end = len(litlist)
    for i in range(begin, end):
        lit = litlist[i]
        node_metrics["good_decision"].append(lit2truth[lit] == node_metrics["T/F"][i])

###################################################################################################################
"Main algorithm"
###################################################################################################################


def DP_algo_naive(CNF, lit, truth, node_metrics, sudoku_metrics):
    cl2truth, lit2truth, lit2cls, atom_count, litlist, choices = CNF

    num_sat_clauses = update_atom_count(cl2truth, lit2truth, atom_count)
    update_node_metrics(node_metrics, truth, atom_count, lit, choices, num_sat_clauses)
    update_sudoku_metrics_temp(sudoku_metrics)
    update_truth_values(lit2truth, lit, truth, choices)  # Update lit2truth

    if satisfied_naive(cl2truth, lit2truth):
        return True
    if empty_clauses_naive(lit2truth, lit2cls, lit):
        return False

    check = unit_clause_simplification(cl2truth, lit2truth, lit2cls)  # Will return true if no conflicts and false o.w.
    if check == False:  # Revert back to the original lit2truth values, because the unit_clause failed
        return False

    if satisfied_naive(cl2truth, lit2truth):
        return True

    lit = choose_value(lit2truth)
    choices[lit] = lit2truth.copy()
    CNF = cl2truth, lit2truth, lit2cls, atom_count, litlist, choices
    return DP_algo_naive(CNF, lit, 1, node_metrics, sudoku_metrics) or DP_algo_naive(CNF, lit, -1, node_metrics, sudoku_metrics)


###################################################################################################################
"Unit clause simplfication"
###################################################################################################################


def unit_clause_simplification(cl2truth, lit2truth, lit2cls):
    unit_list = build_unit_clause_list(cl2truth, lit2truth, lit2cls)
    if unit_list == False:  # If unit_list is not a bool, it will resolve to True. So if unit_list is False then execute
        return False
    while len(unit_list) != 0:
        unit_list = build_unit_clause_list(cl2truth, lit2truth, lit2cls)
        if unit_list == False:
            return False
    return True


def build_unit_clause_list(cl2truth, lit2truth, lit2cls):
    unit_list = []
    for clause in cl2truth:  # TODO Can optimize by checking if clause already satisfied
        if not clause_satisfied(clause, lit2truth):
            unit = unit_clause(lit2truth, clause)
            if unit is not None:
                lit = unit[0]
                truth = unit[1]
                lit2truth[lit] = truth
                if empty_clauses_naive(lit2truth, lit2cls, lit):  # Check if there is a conflict
                    return False
                unit_list.append(unit)
    return unit_list


def unit_clause(lit2truth, clause):
    unit = None
    counter = 0
    for atom in clause:
        lit = abs(atom)
        if lit2truth[lit] == 0:
            counter = counter + 1
            if atom < 0:
                unit = (lit, -1)
            else:
                unit = (lit, 1)
    if counter == 1:
        return unit
    return None


###################################################################################################################
"""For later use maybe"""
###################################################################################################################


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