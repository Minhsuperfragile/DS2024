from flask import Flask, render_template, request
import random

app = Flask(__name__)

def generate_sudoku():
    # Simple static Sudoku grid with some cells empty (0 means empty cell)
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    return board

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the submitted solution
        solution = [[int(request.form[f"cell_{r}_{c}"]) for c in range(9)] for r in range(9)]
        # Validate the solution
        if validate_sudoku(solution):
            return render_template("index.html", board=solution, message="Solution is correct!")
        else:
            return render_template("index.html", board=generate_sudoku(), message="Invalid solution!")
    
    # Default view with an initial puzzle
    board = generate_sudoku()
    return render_template("index.html", board=board, message="Solve the puzzle!")

def validate_sudoku(board):
    # Simplified validation (check rows, columns, and 3x3 grids)
    for r in range(9):
        if not is_valid_group(board[r]):  # Check row
            return False
        if not is_valid_group([board[i][r] for i in range(9)]):  # Check column
            return False
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            grid = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
            if not is_valid_group(grid):  # Check 3x3 grid
                return False
    return True

def is_valid_group(group):
    # Check if a group (row, column, or 3x3 block) contains no duplicates
    group = [x for x in group if x != 0]
    return len(group) == len(set(group))

if __name__ == "__main__":
    app.run(debug=True)
