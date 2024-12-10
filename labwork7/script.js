const puzzle = [
    [5, 3, '', '', 7, '', '', '', ''],
    [6, '', '', 1, 9, 5, '', '', ''],
    ['', 9, 8, '', '', '', '', 6, ''],
    [8, '', '', '', 6, '', '', '', 3],
    [4, '', '', 8, '', 3, '', '', 1],
    [7, '', '', '', 2, '', '', '', 6],
    ['', 6, '', '', '', '', 2, 8, ''],
    ['', '', '', 4, 1, 9, '', '', 5],
    ['', '', '', '', 8, '', '', 7, 9]
];

const solution = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
];

function createGrid() {
    const grid = document.getElementById('sudoku-grid');
    puzzle.forEach((row, rowIndex) => {
        row.forEach((cell, colIndex) => {
            const input = document.createElement('input');
            if (cell !== '') {
                input.value = cell;
                input.disabled = true;
            } else {
                input.value = '';
            }
            input.dataset.row = rowIndex;
            input.dataset.col = colIndex;
            grid.appendChild(input);
        });
    });
}

function checkSolution() {
    const inputs = document.querySelectorAll('#sudoku-grid input');
    let isCorrect = true;

    inputs.forEach(input => {
        const row = input.dataset.row;
        const col = input.dataset.col;
        const value = input.value;

        if (parseInt(value) !== solution[row][col]) {
            isCorrect = false;
        }
    });

    const message = document.getElementById('result-message');
    message.textContent = isCorrect ? 'Congratulations! You solved the puzzle!' : 'There are errors in your solution.';
}

document.getElementById('check-solution').addEventListener('click', checkSolution);

createGrid();
