with open("4x4.txt", "r") as file:
    sudoku = file.readline()

print(sudoku)
row = 1
column = 1

f = open("sudoku-Dimacs.txt", "w")
for number in sudoku:
    if number.isdigit():
        n = str(row) + str(column) + str(number) + " 0\n"
        f.write(n)
    if column == 9:
        row = row + 1
        column = 1
        continue
    column = column + 1
f.close()
