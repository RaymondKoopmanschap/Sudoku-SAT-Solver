
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
