def generate_output_file(inputfile, lit2truth, num_clauses):
    output_file = inputfile + ".out"
    f= open(output_file,"w+")

    f.write("p cnf " + str(len(lit2truth)) + " " + str(num_clauses) + "\n")

    for lit in lit2truth:
        if lit2truth[lit] == 0:
            lit2truth[lit] = 1
        atom = lit * lit2truth[lit]
        f.write(str(atom) + " 0\n")
