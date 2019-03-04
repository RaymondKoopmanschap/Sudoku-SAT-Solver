from random import choice


###################################################################################################################
"Main algorithm"
###################################################################################################################


def davis_putnam(CNF, lit, truth, node_metrics, step_counter, step_counter_node, heuristic ="standard"):
    cl2truth, lit2truth, lit2cls, atom_count, litlist, choices = CNF
    # Updates
    update_truth_values(lit2truth, lit, truth, choices)  # Update lit2truth\
    num_unsat_clauses = update_atom_count(cl2truth, lit2truth, atom_count)
    f, j = update_JWOS_and_MOM(cl2truth, lit2truth, lit2cls)
    update_node_metrics(node_metrics, truth, atom_count, lit, choices, num_unsat_clauses, f, j)
    update_step_counter_temp(step_counter)

    # Checks
    if satisfied_naive(cl2truth, lit2truth):
        return True
    if empty_clauses_naive(lit2truth, lit2cls, lit):
        return False
    check = unit_clause_simplification(cl2truth, lit2truth, lit2cls)  # Will return true if no conflicts and false o.w.
    if check == False:  # Revert back to the original lit2truth values, because the unit_clause failed
        return False
    if satisfied_naive(cl2truth, lit2truth):
        return True

    # Choosing literal
    if heuristic == "standard":
        lit = choose_lit_standard(lit2truth)
    elif heuristic == "random":
        lit = choose_lit_rand(lit2truth)
    elif heuristic == "own":
        lit = choose_lit_own(lit2truth, atom_count)
    elif heuristic == "DLCS":
        lit = choose_lit_DLCS(lit2truth, atom_count)
    elif heuristic == "DLIS":
        lit = choose_lit_DLIS(lit2truth, atom_count)
    elif heuristic == "JWOS":
        lit = choose_lit_JWOS(lit2truth, lit2cls)
    elif heuristic == "MOM":
        lit = choose_lit_MOM(cl2truth, lit2truth, lit2cls)

    choices[lit] = lit2truth.copy()

    CNF = cl2truth, lit2truth, lit2cls, atom_count, litlist, choices
    CP = atom_count[lit]
    CN = atom_count[-lit]

    # Choosing truth value
    if CP < CN:
        return davis_putnam(CNF, lit, -1, node_metrics, step_counter, step_counter_node, heuristic) or davis_putnam(CNF, lit, 1, node_metrics, step_counter, step_counter_node, heuristic)
    else:
        return davis_putnam(CNF, lit, 1, node_metrics, step_counter, step_counter_node, heuristic) or davis_putnam(CNF, lit, -1, node_metrics, step_counter, step_counter_node, heuristic)


###################################################################################################################
"Choice heuristics"
###################################################################################################################
# %% choice heuristics


def choose_lit_standard(lit2truth):
    for lit in lit2truth:
        if lit2truth[lit] == 0:
            return lit


def choose_lit_rand(lit2truth):
    litlist=[]
    for lit in lit2truth:
        if lit2truth[lit] == 0:
            litlist.append(lit)
    return choice(litlist)  # Random choice


def choose_lit_own(lit2truth, atom_count):
    beta_CP = 0.454
    beta_CN = -0.244
    f_max=-1000 # value should be lower than any other value we might encounter
    for lit in lit2truth:
        f_lit = beta_CP*atom_count[lit]+beta_CN*atom_count[-lit]
        if lit2truth[lit] == 0 and f_lit > f_max:
            maxlit = lit
            f_max = f_lit
    return maxlit


def choose_lit_DLCS(lit2truth, atom_count):
    f_max=-1000 # value should be lower than any other value we might encounter
    for lit in lit2truth:
        f_lit = max(atom_count[lit],atom_count[-lit])
        if lit2truth[lit] == 0 and f_lit > f_max:
            maxlit = lit
            f_max = f_lit
    return maxlit


def choose_lit_DLIS(lit2truth, atom_count):
    f_max=-1000 # value should be lower than any other value we might encounter
    for lit in lit2truth:
        f_lit = atom_count[lit]+atom_count[-lit]
        if lit2truth[lit] == 0 and f_lit > f_max:
            max_lit = lit
            f_max = f_lit
    return max_lit


def choose_lit_JWOS(lit2truth, lit2cls):
    max = 0
    max_lit = 0
    j = 0
    for lit in lit2truth:
        if lit2truth[lit] == 0:
            for clause in lit2cls[lit]:
                j += 2**-len(clause)
                if j > max:
                    max = j
                    max_lit = lit
    return max_lit


def choose_lit_MOM(cl2truth, lit2truth, lit2cls):
    k = 1
    min_clause_len = 100000000000000
    max_lit = 0
    max_f = 0
    max_lit = 0
    for clause in cl2truth:
        if not clause_satisfied(clause, lit2truth):
            if len(clause) < min_clause_len:
                min_clause_len = len(clause)
    for lit in lit2truth:
        if lit2truth[lit] == 0:
            f_pos = 0
            f_neg = 0
            for clause in lit2cls[lit]:
                for atom in clause:
                    if lit == atom:
                        f_pos += 1
                    if -lit == atom:
                        f_neg += 1
            f = (f_pos + f_neg)*2**k + f_pos * f_neg
            if f > max_f:
                max_f = f
                max_lit = lit
    return max_lit


def update_JWOS_and_MOM(cl2truth, lit2truth, lit2cls):
    k = 1
    min_clause_len = 100000000000000
    max_f = 0
    max_j = 0
    j = 0
    for clause in cl2truth:
        if not clause_satisfied(clause, lit2truth):
            if len(clause) < min_clause_len:
                min_clause_len = len(clause)

    for lit in lit2truth:
        if lit2truth[lit] == 0:
            f_pos = 0
            f_neg = 0
            for clause in lit2cls[lit]:
                j += 2 ** -len(clause)
                if j > max_j:
                    max_j = j
                for atom in clause:
                    if lit == atom:
                        f_pos += 1
                    if -lit == atom:
                        f_neg += 1
            f = (f_pos + f_neg) * 2 ** k + f_pos * f_neg
            if f > max_f:
                max_f = f
    return max_f, max_j
# %%
###################################################################################################################
"Update values + metrics"
###################################################################################################################


def update_truth_values(lit2truth, lit, truth, choices):
    #  Unassign the last choice you made, because you are higher up in the tree
    for i in choices[lit]:
        lit2truth[i] = choices[lit][i]
    lit2truth[lit] = truth  # Assign new given truth value


def update_node_metrics(node_metrics, truth, atom_count, lit, choices, num_unsat_clauses, f, j):
    """Track desired metrics
    Uncomment lines if you don't want to track them and speed up process"""
    node_metrics["T/F"].append(truth)
    node_metrics["CP"].append(atom_count[lit])
    #node_metrics["max_Count"].append(atom_count)
    node_metrics["CN"].append(atom_count[-lit])
    node_metrics["max_C"].append(max(atom_count.values()))
    node_metrics["choice_depth"].append(len(choices) - 1)
    node_metrics["num_unsat_clauses"].append(num_unsat_clauses)
    node_metrics["lit"].append(lit)
    node_metrics["max_J"].append(j)
    node_metrics["max_f"].append(f)


def update_step_counter_temp(step_counter):
    step_counter["num_steps"] += 1


def update_step_counter(step_counter, step_counter_temp):
    step_counter["num_steps"].append(step_counter_temp["num_steps"])


def update_atom_count(cl2truth, lit2truth, atom_count):
    num_unsat_clauses = 0
    atom_count.clear()
    for clause in cl2truth:
        if not clause_satisfied(clause, lit2truth):
            num_unsat_clauses += 1
            for atom in clause:
                atom_count[atom] += 1
    return num_unsat_clauses


def update_right_decision(lit2truth, node_metrics, step_counter, step_counter_temp):
    litlist = node_metrics["lit"]
    begin = sum(step_counter["num_steps"])  # Do this before updating this num_steps dictionary
    end = len(litlist)  # Total number of lit now in the dictionary
    for i in range(begin, end):
        lit = litlist[i]
        node_metrics["good_decision"].append(lit2truth[lit] == node_metrics["T/F"][i])
        node_metrics["num_steps"].append(step_counter_temp["num_steps"])


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
"Unit clause simplification"
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